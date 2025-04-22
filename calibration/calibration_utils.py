'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to provide routines for adaptive and iterative calibration, especially for indices like the Self-Calibrated PDSI.

Available functions:
    self_calibrated_pdsi(data, initial_parameters)
        Implements iterative calibration to adjust PDSI for local conditions.
    **calibrate_index(index_function, calibration_data, kwargs)
        A generic calibration routine that can adjust parameters for any index function based on calibration datasets.
    update_calibration_parameters(old_params, new_data)
        Refines calibration parameters as new data become available.
'''

import numpy as np
import pandas as pd
from scipy.optimize import minimize

def self_calibrated_pdsi(data, initial_parameters):
    """
    Compute a self-calibrated Palmer Drought Severity Index (PDSI) with iterative adjustment.
    
    This is a simplified example where we adjust parameters to minimize the difference between
    modeled and observed drought severity. In practice, this might involve a water balance model.
    
    Args:
        data: Pandas DataFrame or dict containing observed data (e.g., precipitation, temperature, soil moisture).
        initial_parameters: Dict or array of initial parameters for the calibration model.
        
    Returns:
        calibrated_pdsi: Pandas Series of the self-calibrated PDSI.
        calibrated_params: Optimized parameters.
    """
    
    # Example model: pdsi_model = a * precip + b * temp + c * soil_moisture, with a, b, c parameters.
    # The goal is to minimize the difference between pdsi_model and some target drought indicator.
    
    # Assume target_pdsi is part of the input data.
    target_pdsi = data['target_pdsi']
    precip = data['precip']
    temp = data['temp']
    soil_moisture = data['soil_moisture']
    
    def objective(params):
        a, b, c = params
        model_pdsi = a * precip + b * temp + c * soil_moisture
        error = np.sum((model_pdsi - target_pdsi)**2)
        return error

    # Use initial parameters as a starting point for optimization.
    init_params = [initial_parameters.get('a', 1), initial_parameters.get('b', 1), initial_parameters.get('c', 1)]
    result = minimize(objective, init_params, method='Nelder-Mead')
    calibrated_params = result.x
    a, b, c = calibrated_params
    calibrated_pdsi = a * precip + b * temp + c * soil_moisture
    
    # Return as a Pandas Series if precip is a Series.
    if isinstance(precip, pd.Series):
        calibrated_pdsi = pd.Series(calibrated_pdsi, index=precip.index)
    
    return calibrated_pdsi, {'a': a, 'b': b, 'c': c}

def calibrate_index(index_function, calibration_data, **kwargs):
    """
    A generic calibration routine that adjusts parameters for a given index function.
    
    Args:
        index_function: The function to compute an index.
        calibration_data: Data required for calibration (e.g., observed and modeled values).
        **kwargs: Additional parameters or options for calibration.
    
    Returns:
        best_params: A dictionary of calibrated parameters.
        calibrated_index: The index computed using the calibrated parameters.
    """
    # This is a generic template. In practice, this function could be highly specialized.
    # For demonstration, we'll assume the index_function accepts parameters 'a' and 'b'.
    
    observed = calibration_data['observed']
    input_data = calibration_data['input_data']
    
    def objective(params):
        a, b = params
        modeled = index_function(input_data, a=a, b=b)
        return np.sum((modeled - observed)**2)
    
    # Starting with arbitrary initial parameters (1, 1)
    result = minimize(objective, [1, 1], method='Nelder-Mead')
    best_params = {'a': result.x[0], 'b': result.x[1]}
    calibrated_index = index_function(input_data, **best_params)
    
    return best_params, calibrated_index

def update_calibration_parameters(old_params, new_data):
    """
    Update calibration parameters based on new incoming data.
    
    This function refines existing calibration parameters by comparing model predictions with new observations.
    
    Args:
        old_params: Dictionary of current calibration parameters.
        new_data: Dictionary containing new input data and corresponding observed values.
        
    Returns:
        updated_params: Dictionary of updated calibration parameters.
    """
    # For this simple example, we'll use a weighted average between the old parameters and
    # new parameters derived from new data using a simple regression.
    
    # Assume new_data has keys: 'input' and 'observed'
    from sklearn.linear_model import LinearRegression
    
    X_new = new_data['input']
    y_new = new_data['observed']
    
    # Fit a simple linear regression to new data
    model = LinearRegression()
    model.fit(X_new, y_new)
    new_params = model.coef_
    
    # Assume old_params is a dictionary with keys matching the length of new_params
    updated_params = {}
    weight_old = 0.7
    weight_new = 0.3
    
    for i, key in enumerate(old_params.keys()):
        updated_params[key] = weight_old * old_params[key] + weight_new * new_params[i]
    
    return updated_params
