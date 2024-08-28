import pandas as pd
import numpy as np

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
