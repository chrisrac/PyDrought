'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to implement indices that are crop-specific or aimed at assessing agricultural water needs.

Available functions:
    crop_moisture_index(temperature, precip, crop_parameters)
        Evaluates short-term water stress affecting crops.
    crop_specific_drought_index(crop_data, meteorological_data)
        Tailors drought assessments to specific crop types based on detailed inputs.
    agricultural_reference_index(crop_yields, meteorological_baselines)
        Compares expected vs. actual crop performance under varying conditions.
    water_requirement_satisfaction_index(crop_water_demand, actual_water_supply)
        Assesses whether crops are receiving sufficient water relative to their demand.
'''

def crop_moisture_index(temperature, precip, crop_params):
    '''
    Estimate immediate crop water stress using temperature and precipitation, adjusted by crop parameters.

    Process:
        Combine meteorological data using a formula defined by crop sensitivity; for example, calculate deficits or surpluses relative to crop water needs.
    '''
    # Example: water_stress = (crop_params['optimal_temp'] - temperature) + (crop_params['optimal_precip'] - precip)
    water_stress = (crop_params['optimal_temp'] - temperature) + (crop_params['optimal_precip'] - precip)
    # Optionally, scale or standardize the result
    return water_stress


def crop_specific_drought_index(crop_data, met_data):
    '''
    Generate an index that combines crop-specific growth/yield data with meteorological conditions.
    
    Process:
        Compare observed crop performance against a baseline or expected response given the meteorological conditions.
    '''
    # Placeholder: could be the deviation of actual yield from expected yield based on met conditions.
    expected_yield = met_data['expected_yield']  # Precomputed using a model or baseline
    drought_index = (crop_data - expected_yield) / expected_yield
    return drought_index


def agricultural_reference_index(crop_yields, met_baseline):
    '''
    Assess drought impact by comparing actual crop yields with meteorologically expected yields.
    
    Process:
        Compute the ratio or difference between observed and baseline yields.
    '''
    # Baseline could be an average yield computed from historical data.
    reference_index = crop_yields / met_baseline['mean_yield'] * 100  # as a percentage
    return reference_index


def water_requirement_satisfaction_index(crop_demand, water_supply):
    '''
    Evaluate how well the available water supply meets the crop water demand.
    
    Process:
        Calculate a ratio or a difference; for example, a value of 1 indicates full satisfaction.
    '''

    # Avoid division by zero
    satisfaction_index = np.where(crop_demand != 0, water_supply / crop_demand, np.nan)
    return satisfaction_index
