'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to handle indices requiring streamflow, reservoir, and soil moisture measurements.

Available functions:
    standardized_reservoir_supply_index(reservoir_data, baseline)
        Standardizes reservoir supply data to detect anomalies.
    standardized_streamflow_index(streamflow, baseline)
        Converts streamflow measurements into standardized scores.
    soil_water_storage(soil_moisture_profile, soil_properties)
        Estimates total water stored in the soil given profile data and soil characteristics.
    palmer_hydrological_drought_index(streamflow, runoff, precipitation)
        Extends PDSI concepts to hydrological variables for water supply assessment.
    standardized_water_level_index(water_level_series, baseline)
        Standardizes water-level records (from lakes, reservoirs, etc.) for anomaly detection.
    streamflow_drought_index(streamflow, threshold)
        Identifies drought periods based on low flow conditions using user-defined thresholds.
    surface_water_supply_index(precip, runoff, reservoir_data)
        Aggregates surface water availability from multiple inputs.
'''

def standardized_reservoir_supply_index(reservoir_data, baseline):
    '''
    Compute the standardized anomaly for reservoir supply data to monitor water availability.

    Inputs:
        reservoir_data: Time series (or spatial data) of reservoir inflows/outflows/storage.
        baseline: Long-term average or baseline data.

    Process:
        Calculate the anomaly (observed – baseline) and standardize using the baseline standard deviation.
    '''

    # Assume reservoir_data and baseline are Pandas Series
    anomaly = reservoir_data - baseline['mean']
    standardized_index = anomaly / baseline['std']
    return standardized_index


def standardized_streamflow_index(streamflow, baseline):
    '''
    Convert raw streamflow measurements into standardized values to detect anomalies.

    Inputs:
        streamflow: Time series of streamflow measurements.
        baseline: Long-term mean and standard deviation for streamflow.

    Process:
        Compute z-scores for the streamflow data.
    '''

    # Ensure streamflow is a Pandas Series
    anomaly = streamflow - baseline['mean']
    standardized_index = anomaly / baseline['std']
    return standardized_index


def soil_water_storage(soil_moisture_profile, soil_properties):
    '''
    Estimate the total water stored in a soil profile by integrating moisture content over depth.

    Inputs:
        soil_moisture_profile: Measurements of soil moisture (volumetric water content) at various depths.
        soil_properties: Data on soil layer thickness, bulk density, field capacity, etc.

    Process:
        For each layer, compute water storage as: water content × layer depth × conversion factor.
        Sum over layers.
    '''

    total_storage = 0
    # Assume soil_moisture_profile and soil_properties are dictionaries or DataFrames with matching layers.
    for layer in soil_moisture_profile.keys():
        moisture = soil_moisture_profile[layer]
        depth = soil_properties[layer]['depth']  # in meters
        # Assuming water density factor is 1 (or include conversion if needed)
        storage = moisture * depth
        total_storage += storage
    return total_storage


def palmer_hydrological_drought_index(streamflow, runoff, precip):
    '''
    Adapt the concept of the Palmer Drought Severity Index to hydrological data for water supply assessment.

    Inputs:
        streamflow: Streamflow measurements.
        runoff: Runoff data.
        precip: Precipitation data.

    Process:
        Combine these inputs using a water balance approach.
        Calibrate and standardize to produce a severity index.
    '''

    # Simplified approach: water_balance = precip - (runoff + streamflow loss)
    water_balance = precip - (runoff + streamflow)
    # Standardize water_balance (this could be refined)
    mean_balance = water_balance.mean()
    std_balance = water_balance.std()
    phdsi = (water_balance - mean_balance) / std_balance
    return phdsi


def standardized_water_level_index(water_level_series, baseline):
    '''
    Standardize lake, reservoir, or river water level data to highlight significant deviations.

    Inputs:
        water_level_series: Time series of water level measurements.
        baseline: Baseline water level statistics (mean and std).

    Process:
        Compute z-scores for the water level data.
    '''
    
    anomaly = water_level_series - baseline['mean']
    standardized_index = anomaly / baseline['std']
    return standardized_index


def streamflow_drought_index(streamflow, threshold):
    '''
    Identify drought periods using streamflow data by comparing values against a threshold.

    Inputs:
        streamflow: Streamflow time series.
        threshold: User-defined threshold for low flows (could be absolute or percentile-based).

    Process:
        Compare each streamflow value against the threshold.
        Return a boolean array or a severity scale indicating drought conditions.
    '''

    # Example: return a boolean series where True indicates drought (streamflow < threshold)
    drought_flag = streamflow < threshold
    return drought_flag


def surface_water_supply_index(precip, runoff, reservoir_data, weights=(0.4, 0.3, 0.3)):
    '''
    Create a composite index of surface water supply by aggregating precipitation, runoff, and reservoir data.

    Inputs:
        precip: Precipitation data.
        runoff: Runoff measurements.
        reservoir_data: Reservoir storage or inflow/outflow data.

    Process:
        Combine these inputs using a weighted sum or other aggregation method.
        Normalize the result if needed.
    '''

    # Ensure weights sum to 1.0 or normalize accordingly
    composite = (weights[0]*precip + weights[1]*runoff + weights[2]*reservoir_data)
    # Standardize if necessary
    mean_val = composite.mean()
    std_val = composite.std()
    standardized_composite = (composite - mean_val) / std_val
    return standardized_composite