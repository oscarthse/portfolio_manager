from fastapi import FastAPI
from logic.portfolio import *
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"read message": "PortfolioOptimazationAPI"}

@app.get("/portfolio")
def read_item(stocks, n_simulations):

    n_simulations=int(n_simulations)
    stocks = eval(stocks) #Note: Input should be a list of string with single quotatio f.e. ['AAPL', 'MSFT'....]
    stocks_df = []
    X_fit = []
    y_df= []

    for i in range(len(stocks)):
        stocks_df.append((pd.read_csv(f'stocks_df/stocks_df_{stocks[i]}.csv')).drop(columns = "Unnamed: 0"))
        X_fit.append((pd.read_csv(f'X_fit/X_fit_{stocks[i]}.csv')).drop(columns = "Unnamed: 0"))
        y_df.append((pd.read_csv(f'y_fit/y_df_{stocks[i]}.csv')).drop(columns = "Unnamed: 0"))
    models = load_model(f"models_all_features/model_{stocks[i]}_all_features.keras")
    with open('increments.json', 'r') as f:
        returns = json.load(f)
    cov_matrix = covariance_matrix(stocks_df, stocks)

    returns_plot, vol, sharpe, weights_plot = run_simulations(n_simulations=n_simulations, X_fit = X_fit, time_index=40000, stocks=stocks, covariance_matrix=cov_matrix,models=models, returns=returns)

    return returns_plot, vol, sharpe, weights_plot
