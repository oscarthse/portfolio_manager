import pandas as pd
import numpy as np
from logic.getting import get_price_data_raw
from logic.supporting_functions import rename_columns

def var(simulations, confidence_interval: int):
    '''
    Calculates the worst expected loss at the given confidence level,
    as a percentage of initial investment. For example, a 95% VaR of -2% means
    that there is a 5% chance the asset will lose more than 2% over the time
    the simulations ran.

    Args:
        simulations (np.array): The output of running a GBM algorithm.
        confidence_interval (int): Percentage confidence interval, between 0 and 100

    Returns:
        float: Expected loss as a percentage
    '''
    simulations.sort()
    var = np.percentile(simulations[-1], 100 - confidence_interval)
    loss = (1 - var / simulations[0][0])*100
    return loss


def cvar(simulations, confidence_interval):
    '''
    Calculates the expected loss as a percentage given that the
    loss is beyond the VaR threshold. It provides an average of the worst losses.

    Args:
        simulations (np.array): The output of running a GBM algorithm.
        confidence_interval (int): Percentage confidence interval, between 0 and 100

    Returns:
        float: Expected loss as a percentage
    '''
    simulations.sort()
    var = np.percentile(simulations[-1], 100 - confidence_interval)
    cvar = simulations[simulations <= var].mean()
    loss = (1 - cvar/simulations[0][0]) * 100
    return loss

def volatility(simulations):
    '''
    Calculates the standard deviation of returns,
    reflecting the overall variability or risk of the asset's price.

    Args:
        simulations (np.array): The output of running a GBM algorithm.

    Returns:
        float: The standard deviation of returns.
    '''
    return simulations[-1].std()


def max_drawdown(simulations):
    '''
    Calculates the maximum drawdown

    Parameters:

    Args:
        simulations (np.array): The output of running a GBM algorithm.

    Returns:
        float: The worst loss simulated by GBM as a percentage
    '''
    return np.min(simulations[-1] / np.maximum.accumulate(simulations[-1]) - 1)*100


def ups_and_downs():

    '''
    Returns a dictionary containing the average percentage increase above/below
    the thresholds for the models for each stock.
    '''

    stocks = ['AAPL', 'AMT', 'MSFT', 'CAT', 'GS', 'JNJ', 'MCD', 'NEE', 'PG', 'XOM']
    stocks_df = [0 for i in range(len(stocks))]

    for i in range(len(stocks)):
        stock = get_price_data_raw(stocks[i])
        rename_columns(stock)
        stock = stock.sort_values(by='datetime')
        stocks_df[i] = stock

    percentages = [0 for i in range(len(stocks_df))]

    for i in range(len(stocks_df)):
        stocks_df[i]['percentage_increase'] = (stocks_df[i]['close'] / stocks_df[i]['close'].shift(1) - 1) * 100
        percentages[i] = np.array(stocks_df[i]['percentage_increase'].dropna())
        percentages[i].sort()

    aapl_high = np.array([per for per in percentages[0] if per > 0.07]).mean()
    aapl_low = np.array([per for per in percentages[0] if per < -0.07]).mean()

    amt_high = np.array([per for per in percentages[1] if per > 0.07]).mean()
    amt_low = np.array([per for per in percentages[1] if per < -0.07]).mean()

    msft_high = np.array([per for per in percentages[2] if per > 0.07]).mean()
    msft_low = np.array([per for per in percentages[2] if per < -0.07]).mean()

    cat_high = np.array([per for per in percentages[3] if per > 0.07]).mean()
    cat_low = np.array([per for per in percentages[3] if per < -0.07]).mean()

    gs_high = np.array([per for per in percentages[4] if per > 0.07]).mean()
    gs_low = np.array([per for per in percentages[4] if per < -0.07]).mean()

    jnj_high = np.array([per for per in percentages[5] if per > 0.07]).mean()
    jnj_low = np.array([per for per in percentages[5] if per < -0.07]).mean()

    mcd_high = np.array([per for per in percentages[6] if per > 0.07]).mean()
    mcd_low = np.array([per for per in percentages[6] if per < -0.07]).mean()

    nee_high = np.array([per for per in percentages[7] if per > 0.07]).mean()
    nee_low = np.array([per for per in percentages[7] if per < -0.07]).mean()

    pg_high = np.array([per for per in percentages[8] if per > 0.07]).mean()
    pg_low = np.array([per for per in percentages[8] if per < -0.07]).mean()

    xom_high = np.array([per for per in percentages[9] if per > 0.07]).mean()
    xom_low = np.array([per for per in percentages[9] if per < -0.07]).mean()

    returns = {}
    returns['AAPL'] = {'up': aapl_high, 'down': aapl_low}
    returns['AMT'] = {'up': amt_high, 'down': amt_low}
    returns['MSFT'] = {'up': msft_high, 'down': msft_low}
    returns['CAT'] = {'up': cat_high, 'down': cat_low}
    returns['GS'] = {'up': gs_high, 'down': gs_low}
    returns['JNJ'] = {'up': jnj_high, 'down': jnj_low}
    returns['MCD'] = {'up': mcd_high, 'down': mcd_low}
    returns['NEE'] = {'up': nee_high, 'down': nee_low}
    returns['PG'] = {'up': pg_high, 'down': pg_low}
    returns['XOM'] = {'up': xom_high, 'down': xom_low}

    return returns


def expected_return(model, X_pred, up, down):
    '''
    Returns the model's expected return of the given stock
    '''
    predictions = model.predict(X_pred)
    gain = predictions[0][0]
    loss = predictions[0][2]

    return gain*up + loss*down
