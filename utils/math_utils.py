'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to provide common mathematical operations shared across modules.

Available functions:
    calculate_mean(data)
        Computes the mean value of a dataset.
    calculate_std(data)
        Computes the standard deviation.
    normalize(data, method='zscore' or 'minmax')
        Normalizes data using the chosen method.
    error_propagation(values, uncertainties)
        Performs error propagation calculations for indices that depend on multiple measurements.
'''

import numpy as np
import pandas as pd

def calculate_mean(data):
    """
    Calculate the mean of the input data.

    Args:
        data: Array-like, Pandas Series, or DataFrame.

    Returns:
        The mean value.
    """
    if isinstance(data, (pd.Series, pd.DataFrame)):
        return data.mean()
    else:
        return np.mean(data)

def calculate_std(data):
    """
    Calculate the standard deviation of the input data.

    Args:
        data: Array-like, Pandas Series, or DataFrame.

    Returns:
        The standard deviation.
    """
    if isinstance(data, (pd.Series, pd.DataFrame)):
        return data.std()
    else:
        return np.std(data)

def normalize(data, method='zscore'):
    """
    Normalize the data using the specified method.

    Args:
        data: Array-like, Pandas Series, or DataFrame.
        method: 'zscore' for standard score normalization or 'minmax' for min-max scaling.

    Returns:
        Normalized data.
    """
    if method == 'zscore':
        mean_val = calculate_mean(data)
        std_val = calculate_std(data)
        return (data - mean_val) / std_val
    elif method == 'minmax':
        if isinstance(data, (pd.Series, pd.DataFrame)):
            min_val = data.min()
            max_val = data.max()
        else:
            min_val = np.min(data)
            max_val = np.max(data)
        return (data - min_val) / (max_val - min_val)
    else:
        raise ValueError("Normalization method must be 'zscore' or 'minmax'.")

def error_propagation(values, uncertainties, operation='sum'):
    """
    Calculate propagated uncertainty for an operation.

    For addition/subtraction, the uncertainties add in quadrature.
    For multiplication/division, the relative uncertainties add in quadrature.

    Args:
        values: List or array of values.
        uncertainties: List or array of uncertainties corresponding to each value.
        operation: 'sum' for addition/subtraction or 'product' for multiplication/division.

    Returns:
        Propagated uncertainty.
    """
    values = np.array(values)
    uncertainties = np.array(uncertainties)
    
    if operation == 'sum':
        return np.sqrt(np.sum(uncertainties**2))
    elif operation == 'product':
        # Calculate relative uncertainties
        rel_uncertainties = uncertainties / values
        total_rel_uncertainty = np.sqrt(np.sum(rel_uncertainties**2))
        product_value = np.prod(values)
        return abs(product_value) * total_rel_uncertainty
    else:
        raise ValueError("Operation must be 'sum' or 'product'.")