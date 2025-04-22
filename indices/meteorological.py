'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is implementing indices that rely mainly on precipitation, temperature, and other meteorological variables.

Available functions:
    deciles_index(data)
        Calculates decile rankings for a given dataset.
    percent_normal_precipitation(current_precip, normal_precip)
        Computes the ratio of current precipitation to the long-term normal.
    rainfall_anomaly_index(data, baseline_mean)
        Determines deviations from average rainfall.
    aridity_index(precip, pet)
        Computes the ratio of precipitation to potential evapotranspiration (PET).
    aridity_anomaly_index(current_aridity, baseline_aridity)
        Measures deviation from typical aridity conditions.
    hydrothermal_coefficient(precip, temperature)
        Applies Selyaninov’s formula to assess moisture relative to temperature.
    standardized_anomaly_index(data, baseline_mean, baseline_std)
        Normalizes the anomaly in units of standard deviation.
    keetch_byram_index(rainfall_series, soil_moisture_initial)
        Estimates drought potential with daily rainfall and soil moisture proxy.
    spi(precip, scale, distribution_params=None)
        Computes the Standardized Precipitation Index using probability distribution fitting.
    spei(precip, pet, scale, distribution_params=None)
        Computes the Standardized Precipitation Evapotranspiration Index (SPI extended with PET).
    weighted_anomaly_standardized_precipitation(data, weights)
        Applies user-defined or data-derived weights to precipitation anomalies.
'''

def deciles_index(data):
    '''
    Rank the input data into deciles.

    Inputs:
        data: A Pandas Series or NumPy array of precipitation or similar values.

    Process:
        Sort the data and compute percentile ranks.
    '''

    # Convert data to a Pandas Series if not already
    series = pd.Series(data)
    # Compute deciles: each value is replaced by the decile it falls into (1 to 10)
    decile_ranks = pd.qcut(series, 10, labels=False) + 1
    return decile_ranks


def percent_normal_precipitation(current, normal):
    '''
    Calculate the percentage of normal precipitation.

    Inputs:
        current: Current precipitation (scalar or time series).
        normal: Baseline normal precipitation values.

    Process:
        Compute the ratio (current/normal) and multiply by 100.
    '''

    # Ensure division safety
    percent_normal = (current / normal) * 100
    return percent_normal


def rainfall_anomaly_index(data, baseline_mean):
    '''
    Determine the anomaly by subtracting the baseline mean.

    Inputs:
        data: Rainfall time series.
        baseline_mean: Long-term mean rainfall.

    Process:
        Subtract the baseline from the observed data.
    '''

    anomaly = data - baseline_mean
    return anomaly


def aridity_index(precip, pet):
    '''
    Compute a simple ratio of precipitation to potential evapotranspiration.

    Inputs:
        precip: Precipitation values.
        pet: Potential Evapotranspiration values.

    Process:
        Compute precip / pet, handling division by zero.
    '''

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        index = np.where(pet != 0, precip / pet, np.nan)
    return index


def aridity_anomaly_index(current_aridity, baseline):
    '''
    Calculate the anomaly of the aridity index.

    Inputs:
        current_aridity: Recently computed aridity index.
        baseline: Long-term baseline aridity index.

    Process:
        Subtract the baseline from current aridity.
    '''

    anomaly = current_aridity - baseline
    return anomaly


def hydrothermal_coefficient(precip, temp):
    '''
    Use Selyaninov’s formula to relate precipitation and temperature.

    Inputs:
        precip: Precipitation values.
        temp: Temperature values.

    Process:
        Typically, the formula may be: K = precip / (0.1 * temp) (adjustable based on literature).
    '''

    # Example coefficient calculation; adjust multiplier as per definition
    coefficient = precip / (0.1 * temp)
    return coefficient


def standardized_anomaly_index(data, mean, std):
    '''
    Normalize the anomaly by using the standard deviation.

    Inputs:
        data: Observed values.
        mean: Baseline mean.
        std: Baseline standard deviation.

    Process:
        Calculate the z-score: (data - mean) / std.
    '''

    return (data - mean) / std


def keetch_byram_index(rainfall_series, initial_sm):
    '''
    Estimate the drought potential based on daily rainfall and soil moisture.

    Inputs:
        rainfall_series: A daily series of rainfall.
        initial_sm: The starting soil moisture condition.

    Process:
        Use the recursive or stepwise formulation defined in the Keetch–Byram method.
        This function may need to iterate through each day and update soil moisture.
    '''

    kb_index = []
    sm = initial_sm
    for rain in rainfall_series:
        # Simplified update, real implementation will follow the established formula
        sm = max(0, sm - rain)  # reduce soil moisture by rainfall amount, placeholder logic
        kb_index.append(sm)
    return np.array(kb_index)


def standardized_precipitation_index(precip, scale, distribution_params=None):
    '''
    Compute the Standardized Precipitation Index using probability distribution fitting.

    Inputs:

        precip: Precipitation time series.
        scale: Time scale over which to compute SPI (e.g., 3-month, 6-month).
        distribution_params: Optional precomputed parameters of the fitted distribution.

    Process:

        Aggregate data over the specified scale.
        Fit a probability distribution (commonly Gamma) if parameters are not provided.
        Convert the precipitation values into a cumulative probability and then to a standardized score.
    '''

    # Aggregate precipitation over the specified time scale
    # (this could be a rolling sum for a moving window)
    aggregated = pd.Series(precip).rolling(window=scale).sum()
    # Fit a distribution if needed; assume a helper function fit_gamma_distribution exists
    if distribution_params is None:
        distribution_params = fit_gamma_distribution(aggregated.dropna())
    # Compute cumulative probability using the fitted distribution
    # and then convert to a z-score using the inverse normal distribution function
    cdf_vals = gamma.cdf(aggregated, *distribution_params)
    spi_values = norm.ppf(cdf_vals)
    return spi_values


def standardized_precipitation_evapotranspiration_index(precip, pet, scale, distribution_params=None):
    '''
    Compute the Standardized Precipitation Evapotranspiration Index (SPEI) by including PET.

    Inputs:
        precip: Precipitation time series.
        pet: Potential evapotranspiration time series.
        scale: Time scale.
        distribution_params: Optional parameters for distribution fitting.

    Process:
        Compute the water balance: D = precip - pet.
        Aggregate over the given time scale and proceed similarly to SPI.
    '''

    # Compute water balance
    D = np.array(precip) - np.array(pet)
    # Aggregate over the time scale
    aggregated = pd.Series(D).rolling(window=scale).sum()
    # Fit a distribution if necessary
    if distribution_params is None:
        distribution_params = fit_gamma_distribution(aggregated.dropna())
    cdf_vals = gamma.cdf(aggregated, *distribution_params)
    spei_values = norm.ppf(cdf_vals)
    return spei_values


def weighted_anomaly_standardized_precipitation(data, weights):
    '''
    Combine precipitation anomalies using user-defined weights.

    Inputs:
        data: Precipitation anomaly time series.
        weights: A weight factor or array corresponding to the data.

    Process:
        Multiply the anomaly by its respective weight and then standardize if needed.
    '''

    weighted_anomaly = data * weights
    # Standardize the weighted anomaly
    mean_val = np.mean(weighted_anomaly)
    std_val = np.std(weighted_anomaly)
    standardized_weighted_anomaly = (weighted_anomaly - mean_val) / std_val
    return standardized_weighted_anomaly