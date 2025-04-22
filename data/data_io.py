'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

data/data_io.py 
The purpose of this module is reading and converting data formats into a consistent structure.

Available functions:
    read_csv(filepath, kwargs)
        Reads meteorological or hydrological data stored in CSV files.
    read_netcdf(filepath, variable, kwargs)
        Extracts data from NetCDF files, useful for gridded or satellite data.
    read_geotiff(filepath, kwargs)
        Loads remote sensing imagery data (e.g., for NDVI or EVI).
    read_json(filepath, kwargs)
        Parses JSON formatted data, if applicable for metadata or ancillary information.
'''

import pandas as pd
import xarray as xr
import rasterio
import json


def read_csv(filepath, **kwargs):
    """
    Reads a CSV file and returns a Pandas DataFrame.
    """
    try:
        df = pd.read_csv(filepath, **kwargs)
        return df
    except Exception as e:
        raise IOError(f"Error reading CSV file {filepath}: {e}")


def read_netcdf(filepath, variable, **kwargs):
    """
    Reads a NetCDF file and returns the specified variable as an xarray DataArray.
    """
    try:
        ds = xr.open_dataset(filepath, **kwargs)
        data = ds[variable]
        return data
    except Exception as e:
        raise IOError(f"Error reading NetCDF file {filepath}: {e}")


def read_geotiff(filepath, **kwargs):
    """
    Reads a GeoTIFF file and returns the raster data and metadata.
    """
    try:
        with rasterio.open(filepath, **kwargs) as src:
            data = src.read(1)  # assuming single band data
            meta = src.meta
        return data, meta
    except Exception as e:
        raise IOError(f"Error reading GeoTIFF file {filepath}: {e}")


def read_json(filepath, **kwargs):
    """
    Reads a JSON file and returns the parsed content.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f, **kwargs)
        return data
    except Exception as e:
        raise IOError(f"Error reading JSON file {filepath}: {e}")