'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is computing indices based on remote sensing data.

Available functions:
    ndvi(nir, red)
        Calculates the Normalized Difference Vegetation Index from near-infrared and red bands.
    evi(nir, red, blue, g=2.5, c1=6, c2=7.5, L=1)
        Computes the Enhanced Vegetation Index with adjustments for atmospheric effects.
    savi(nir, red, L=0.5)
        Calculates the Soil Adjusted Vegetation Index to reduce soil brightness effects.
    evaporative_stress_index(thermal_data, vegetation_data)
        Derives an index of vegetation water stress from thermal anomalies.
    vegetation_condition_index(vegetation_timeseries)
        Assesses temporal changes in vegetation condition.
    vegetation_health_index(spectral_bands)
        Combines multiple spectral inputs to assess overall vegetation health.
'''

def ndvi(nir, red):
    '''
    Compute NDVI as (NIR – Red) / (NIR + Red).
    '''
    # Avoid division by zero by adding a small epsilon if necessary
    epsilon = 1e-10
    return (nir - red) / (nir + red + epsilon)


def evi(nir, red, blue, g=2.5, c1=6, c2=7.5, L=1):
    '''
    Compute EVI using the formula: EVI = g * ((nir - red) / (nir + c1 * red - c2 * blue + L))
    '''
    return g * ((nir - red) / (nir + c1 * red - c2 * blue + L))


def savi(nir, red, L=0.5):
    '''
    Compute SAVI as ((nir - red) / (nir + red + L)) * (1 + L).
    '''
    return ((nir - red) / (nir + red + L)) * (1 + L)


def evaporative_stress_index(thermal_data, veg_data):
    '''
    Derive vegetation water stress by combining thermal data (indicative of heat) with vegetation indices.
    '''
    # Placeholder: a higher thermal value relative to vegetation greenness may indicate stress.
    return thermal_data / (veg_data + 1e-10)


def vegetation_condition_index(veg_timeseries):
    '''
    Analyze the temporal behavior of vegetation by computing trends or deviations from a baseline.
    '''
    # A simple approach could be to compute a rolling mean anomaly.
    baseline = veg_timeseries.rolling(window=30, min_periods=1).mean()
    condition_index = veg_timeseries - baseline
    return condition_index


def vegetation_health_index(spectral_bands):
    '''
    Combine multiple spectral bands to produce a composite health score.

    Inputs:
        spectral_bands: A dictionary (or similar structure) with keys like 'red', 'nir', 'blue', etc.
    '''
    # Example: use a weighted combination of NDVI and EVI
    ndvi_val = ndvi(spectral_bands['nir'], spectral_bands['red'])
    evi_val = evi(spectral_bands['nir'], spectral_bands['red'], spectral_bands.get('blue', None))
    # Combine with arbitrary weights (can be parameterized)
    health_index = 0.6 * ndvi_val + 0.4 * evi_val
    return health_index



