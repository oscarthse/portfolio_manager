import numpy as np
import pandas as pd
from logic.getting import *
from logic.supporting_functions import *
from logic.final_preproc_function import *
from logic.scaler import *
from logic.stats import expected_return, ups_and_downs
from pypfopt.risk_models import risk_matrix, fix_nonpositive_semidefinite, cov_to_corr, CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

def merged_times(stocks: list):
    '''
    Inner merges the time on the given stocks

    Args:
        stocks (list): List of strings containing the exact names of the stocks (e.g 'AAPL').

    Returns:
        list of pd.DataFrame: two lists of dataframes containing the features
        and targets of each stock aligned on timestamp
    '''
    stocks_df = [0 for i in range(len(stocks))]
    X_df= [0 for i in range(len(stocks))]
    y_df = [0 for i in range(len(stocks))]

    for i in range(len(stocks)):
        stock_raw = get_price_data_raw(stocks[i])
        stock_tech = get_technical_analysis(stocks[i])
        stock_macro = get_macro_data()
        X, y, log_df = create_x_y(stock_raw, stock_tech, stock_macro)
        rename_columns(stock_raw)
        stock = stock.sort_values(by='datetime')
        stocks_df[i] = stock_raw
        X_df[i] = X
        y_df[i] = y

    df = stocks_df[0].filter(['datetime'])

    for stock in stocks_df[1:]:
        df = df.merge(stock.filter(['datetime']), on= 'datetime', how= 'inner')



    X_fit = [X_df[i] for i in range(10)]
    for i in range(10):
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
    cov = risk_matrix(df)
    shr = CovarianceShrinkage(df, frequency = 252*20)
    shr = shr.ledoit_wolf()
    return shr

def optimize(X_fit, time_index, stocks, covariance_matrix):
    returns = ups_and_downs()
    models = [0 for i in range(len(stocks))]
    for i in range(len(stocks)):
        models[i] = get_neural_nets(stocks[i])

        X_pred = X_fit[i][time_index:time_index + 1]
        scale = initialize_scaler(X_fit[i])
        X_pred = transform_scaler(scale, X_pred)
        X_fit[i] = expected_return(models[i], X_pred, returns[stocks[i]]['up'], returns[stocks[i]]['down'])

    ef = EfficientFrontier(X_fit, covariance_matrix)
    ef.max_sharpe()
    cleaned_weights = ef.clean_weights()

    return cleaned_weights, ef.portfolio_performance(verbose = True)
