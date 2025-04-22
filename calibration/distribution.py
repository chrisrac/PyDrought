'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to fit probability distributions to data, critical for SPI, SPEI, and other indices.

Available functions:
    fit_gamma_distribution(data)
        Fits a gamma distribution to precipitation or other skewed data.
    fit_weibull_distribution(data)
        Fits a Weibull distribution, if appropriate for the dataset.
    fit_log_normal_distribution(data)
        Fits a log-normal distribution to the input data.
    fit_distribution(data, distribution_type)
        General function to choose and fit a specified distribution type.
'''

import numpy as np
import scipy.stats as stats

def fit_gamma_distribution(data):
    """
    Fit a Gamma distribution to the provided data.

    Args:
        data: 1D array-like data (e.g., aggregated precipitation).

    Returns:
        Tuple of fitted parameters: (shape, loc, scale).
    """
    data = np.asarray(data)
    # Gamma is defined for positive values only
    data = data[data > 0]
    shape, loc, scale = stats.gamma.fit(data)
    return shape, loc, scale

def fit_weibull_distribution(data):
    """
    Fit a Weibull distribution to the provided data.

    Args:
        data: 1D array-like data.

    Returns:
        Tuple of fitted parameters: (shape, loc, scale).
    """
    data = np.asarray(data)
    data = data[data > 0]
    shape, loc, scale = stats.weibull_min.fit(data)
    return shape, loc, scale

def fit_log_normal_distribution(data):
    """
    Fit a Log-Normal distribution to the provided data.

    Args:
        data: 1D array-like data.

    Returns:
        Tuple of fitted parameters: (shape, loc, scale).
    """
    data = np.asarray(data)
    data = data[data > 0]
    shape, loc, scale = stats.lognorm.fit(data)
    return shape, loc, scale

def fit_distribution(data, distribution_type='gamma'):
    """
    Fit the specified distribution to the data.

    Args:
        data: 1D array-like data.
        distribution_type: One of 'gamma', 'weibull', or 'lognormal'.

    Returns:
        Fitted distribution parameters.
    """
    if distribution_type == 'gamma':
        return fit_gamma_distribution(data)
    elif distribution_type == 'weibull':
        return fit_weibull_distribution(data)
    elif distribution_type == 'lognormal':
        return fit_log_normal_distribution(data)
    else:
        raise ValueError("Unsupported distribution type. Choose 'gamma', 'weibull', or 'lognormal'.")