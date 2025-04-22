'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

data/preprocessing.py 
The purpose of this module is data cleaning, normalization, and baseline computation.

Available functions:
    compute_long_term_mean(data, period)
        Calculates the baseline mean (e.g., for precipitation or temperature) over a specified period.
    compute_long_term_std(data, period)
        Calculates the standard deviation used in standardized indices.
    detrend_data(data, method='linear')
        Removes trends from time series to focus on anomalies.
    normalize_data(data, method='minmax' or 'zscore')
        Standardizes data for indices that require normalization.
    fill_missing_data(data, method='interpolate')
        Handles gaps or missing values to ensure complete datasets.
'''

import numpy as np
import pandas as pd
from scipy.signal import detrend


def compute_long_term_mean(data, period=None):
    """
    Computes the long-term mean of the data.
    If period is specified (e.g., 'M' for monthly), computes a grouped mean.
    """
    if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
        if period:
            return data.groupby(data.index.to_period(period)).mean()
        return data.mean()
    elif isinstance(data, np.ndarray):
        return np.mean(data)
    else:
        raise ValueError("Unsupported data type for computing mean")


def compute_long_term_std(data, period=None):
    """
    Computes the long-term standard deviation of the data.
    """
    if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
        if period:
            return data.groupby(data.index.to_period(period)).std()
        return data.std()
    elif isinstance(data, np.ndarray):
        return np.std(data)
    else:
        raise ValueError("Unsupported data type for computing standard deviation")
    

def detrend_data(data, method='linear'):
    """
    Removes trends from the data. For now, linear detrending is implemented.
    """
    if method == 'linear':
        if isinstance(data, pd.Series):
            return pd.Series(detrend(data.values), index=data.index)
        elif isinstance(data, np.ndarray):
            return detrend(data)
        else:
            raise ValueError("Unsupported data type for detrending")
    else:
        raise NotImplementedError(f"Method '{method}' is not implemented")
    

def normalize_data(data, method='zscore'):
    """
    Normalizes data using z-score or min-max normalization.
    """
    if method == 'zscore':
        mean_val = compute_long_term_mean(data)
        std_val = compute_long_term_std(data)
        if isinstance(data, pd.Series):
            return (data - mean_val) / std_val
        elif isinstance(data, np.ndarray):
            return (data - mean_val) / std_val
    elif method == 'minmax':
        min_val = data.min() if hasattr(data, 'min') else np.min(data)
        max_val = data.max() if hasattr(data, 'max') else np.max(data)
        return (data - min_val) / (max_val - min_val)
    else:
        raise ValueError("Normalization method must be 'zscore' or 'minmax'")
    

def fill_missing_data(data, method='interpolate'):
    """
    Fills missing data using the specified method.
    Currently supports 'interpolate', 'ffill' (forward-fill) or 'bfill' (backward-fill).
    """
    if isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
        if method == 'interpolate':
            return data.interpolate()
        elif method == 'ffill':
            return data.fillna(method='ffill')
        elif method == 'bfill':
            return data.fillna(method='bfill')
        else:
            raise ValueError("Method not supported for filling missing data")
    else:
        raise ValueError("Unsupported data type for filling missing data")