from fastapi import FastAPI
from logic.portfolio import *
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"read message": "PortfolioOptimazationAPI"}

@app.get("/portfolio")
def read_item(stocks):

    stocks = eval(stocks) #Note: Input should be a list of string with single quotatio f.e. ['AAPL', 'MSFT'....]
    stocks_df = []
    X_fit = []
    y_df= []

    for i in range(len(stocks)):
        stocks_df.append((pd.read_csv(f'stocks_df/stocks_df_{stocks[i]}.csv')).drop(columns = "Unnamed: 0"))
        X_fit.append((pd.read_csv(f'X_fit/X_fit_{stocks[i]}.csv')).drop(columns = "Unnamed: 0"))
        y_df.append((pd.read_csv(f'y_fit/y_df_{stocks[i]}.csv')).drop(columns = "Unnamed: 0"))
    models = get_many_models(stocks)
    with open('increments.json', 'r') as f:
        returns = json.load(f)
    cov_matrix = covariance_matrix(stocks_df, stocks)

    cleaned_weights, performance = optimize(X_fit, time_index=40000, stocks=stocks, covariance_matrix=cov_matrix, models=models, returns=returns)

    response = {"weights": cleaned_weights,"performance": {"expected_return": performance[0], "volatility": performance[1],"sharpe_ratio": performance[2]}}

    return response
