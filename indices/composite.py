'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to build more complex, integrative indices from multiple datasets.

Available functions:
    combined_drought_indicator(index_values, weights)
        Aggregates several drought indices into one composite measure using weighted averages.
    multivariate_standardized_drought_index(input_dict)
        Performs a multivariate analysis by combining various standardized variables (e.g., precipitation, temperature, soil moisture).
'''

def combined_drought_indicator(index_values, weights):
    '''
    Combine several drought indices into one composite measure using weighted averages.

    Process:
        Multiply each index by its weight and sum the results; optionally standardize the final index.
    '''

    # Assume index_values is a dictionary with keys as index names and values as Pandas Series.
    # weights is a dictionary with matching keys and weight values (summing to 1)
    composite = sum(weights[k] * index_values[k] for k in index_values)
    # Optionally standardize composite using utils normalization routines
    mean_val = composite.mean()
    std_val = composite.std()
    composite_standardized = (composite - mean_val) / std_val
    return composite_standardized


def multivariate_standardized_drought_index(input_dict):
    '''
    Create a holistic drought index by integrating several standardized variables.

    Process:
        Apply a multivariate statistical method (e.g., principal component analysis or simple weighted summation) to combine the inputs.
    '''
    
    # input_dict keys: 'precip', 'temperature', 'soil_moisture', etc.
    # Each value should be a standardized time series (z-scores)
    # Example using a simple average of available standardized variables:
    variables = list(input_dict.values())
    combined = sum(variables) / len(variables)
    return combined
