import pandas as pd
import numpy as np

def gbm(close_prices, last_data_point, window_size=5000, n = 1000, T = 100, M = 1000):

    '''
    Runs M (default 1000) GBM simulations starting at the last_data_point
    index of the input data

    Args:
        close_prices (pd.Series): Pandas series containing the close prices of the desired stock
        last_data_point (int): Index of the data point to start simulations from
        window_size (int): Size of the window of time to calculate drift and volatility
        n (int): Number of random steps to simulate
        T (int): Time in 30-minute intervals
        M (int) = Number of paths to simulate

    Returns:
        np.array: A 2D array containing the trajectories of all simulated paths
    '''

    # Calculate log returns
    log_returns = np.log(close_prices / close_prices.shift(1))
    # Drift coefficient
    mu = log_returns[last_data_point - window_size : last_data_point].mean()
    # Volatility
    sigma = log_returns[last_data_point - window_size : last_data_point].std()
    # Initial stock price
    S0 = close_prices[last_data_point]
    # Calculate each time step
    dt = T/n

    # Simulation using numpy arrays
    St = np.exp(
        (mu - sigma ** 2 / 2) * dt
        + sigma * np.random.normal(0, np.sqrt(dt), size=(M,n)).T
    )
    # Include array of 1's
    St = np.vstack([np.ones(M), St])
    # Mulltiply through by S0 and return the cumulative product
    # of elements along a given simulation path (axis=0).
    St = S0 * St.cumprod(axis=0)

    return St
