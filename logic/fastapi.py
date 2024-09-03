from fastapi import FastAPI
from logic.portfolio import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"read message": "PortfolioOptimazationAPI"}

@app.get("/portfolio")
def read_item(stocks):

    stocks = eval(stocks) #Note: Input should be a list of string with single quotatio f.e. ['AAPL', 'MSFT'....]

    X_fit, y_df, stocks_df = merged_times(stocks)
    cov_matrix = covariance_matrix(stocks_df, stocks)
    cleaned_weights, performance = optimize(X_fit, time_index=40000, stocks=stocks, covariance_matrix=cov_matrix)
    response = {"weights": cleaned_weights,"performance": {"expected_return": performance[0], "volatility": performance[1],"sharpe_ratio": performance[2]}}

    return response
