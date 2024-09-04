import numpy as np
import pandas as pd
from logic.getting import *
from logic.supporting_functions import *
from logic.final_preproc_function import *
from logic.scaler import *
from logic.stats import expected_return, ups_and_downs
from pypfopt.risk_models import risk_matrix, fix_nonpositive_semidefinite, cov_to_corr, CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from tensorflow.keras.models import load_model



def merged_times(stocks: list):
    stocks_df = [0 for i in range(len(stocks))]
    X_df= [0 for i in range(len(stocks))]
    y_df = [0 for i in range(len(stocks))]

    for i in range(len(stocks)): #stocks[i]
        stock_raw, = get_price_data_raw(stocks[i])
        stock_tech = get_technical_analysis(stocks[i])
        stock_macro = get_macro_data()
        X, y, log_df = create_x_y(stock_raw, stock_tech, stock_macro)
        rename_columns(stock_raw)
        stock_raw = stock_raw.sort_values(by='datetime')
        stocks_df[i] = stock_raw
        X_df[i] = X
        y_df[i] = y

    df = stocks_df[0].filter(['datetime'])

    for stock in stocks_df[1:]:
        df = df.merge(stock.filter(['datetime']), on= 'datetime', how= 'inner')


    X_fit = [X_df[i] for i in range(len(stocks))]
    for i in range(len(stocks)):
        stocks_df[i] = stocks_df[i].sort_values(by = 'datetime')
        stocks_df[i] = stocks_df[i].reset_index()
        stocks_df[i] = stocks_df[i].drop(columns='index')
        stocks_df[i] = stocks_df[i].merge(df, how = 'inner', on = 'datetime')
        stocks_df[i]['combo'] = stocks_df[i]['volume'] - stocks_df[i]['close']
        X_fit[i]['combo'] = X_fit[i]['volume'] - X_fit[i]['close']
        X_fit[i] = stocks_df[i].filter(['datetime', 'combo']).merge(X_fit[i], how = 'inner', on = 'combo')
        X_fit[i] = X_fit[i].sort_values(by = 'datetime')
        X_fit[i] = X_fit[i].reset_index(drop = True)
        X_fit[i] = X_fit[i].drop(columns = ['combo', 'datetime'])

    return X_fit, y_df, stocks_df



def covariance_matrix(stocks_df, stocks):
    df = stocks_df[0].filter(['datetime', 'close'])
    for i in range(1, len(stocks)):
        df = df.merge(stocks_df[i].filter(['close', 'datetime']), on= 'datetime', how= 'inner')
        df = df.rename(columns = {'close_x': stocks[i-1]})
        df = df.rename(columns = {'close_y': stocks[i]})
    df = df.set_index('datetime')
    shr = CovarianceShrinkage(df, frequency = 252*20)
    shr = shr.ledoit_wolf()
    return shr


def get_many_models(stocks):

    models = [0 for i in range(len(stocks))]
    for i in range(len(stocks)):
        models[i] = load_model(f"models_all_features/model_{stocks[i]}_all_features.keras")
    return models


def optimize(X_fit, time_index, stocks, covariance_matrix, models, returns):
    X_opt = X_fit.copy()
    for i in range(len(stocks)):
        X_pred = X_fit[i][time_index:time_index + 1]
        scale = initialize_scaler(X_fit[i])
        X_pred = transform_scaler(scale, X_pred)
        X_opt[i] = expected_return(models[i], X_pred, returns[stocks[i]]['up'], returns[stocks[i]]['down'])

    ef = EfficientFrontier(X_opt, covariance_matrix)
    ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    return cleaned_weights, ef.portfolio_performance(verbose = True)


def run_simulations(n_simulations, X_fit, time_index, stocks, covariance_matrix, models, returns):
    returns_plot = []
    vol = []
    sharpe = []
    weights_plot = []
    for k in range(n_simulations):
        n = time_index + k
        weights, performance = optimize(X_fit, n, stocks, covariance_matrix, models, returns)
        returns_plot.append(performance[0])
        vol.append(performance[1])
        sharpe.append(performance[2])
        weights_plot.append(weights)
 
    return returns_plot, vol, sharpe, weights_plot
