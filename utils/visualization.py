'''
PyDrought
by: Krzysztof Raczynski
citation: Raczynski K., Cartwright J., 2025, PyDrought: an automated library for drought indicies. SoftwareX.

indices/meteorological.py 
The purpose of this module is to generate plots for time series, spatial maps, and composite indicators.

Available functions:
    plot_time_series(time, data, title, xlabel, ylabel)
        Plots time series data for a single index or variable.
    plot_spatial_map(data, coordinates, title, cmap='viridis')
        Visualizes spatial data, for example, showing regional drought severity.
    plot_composite_index(time, indices, labels)
        Overlays multiple drought indices on one graph to compare trends.
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_time_series(time, data, title="Time Series", xlabel="Time", ylabel="Value", figsize=(10, 5)):
    """
    Plot a time series.

    Args:
        time: Array-like of datetime objects or indices.
        data: Array-like or Pandas Series of data values.
        title: Title of the plot.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        figsize: Figure size tuple.

    Returns:
        Matplotlib figure and axis objects.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time, data, marker='o', linestyle='-')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.tight_layout()
    return fig, ax

def plot_spatial_map(data, coordinates, title="Spatial Map", cmap='viridis', figsize=(8, 6)):
    """
    Plot a spatial map using given data and coordinates.

    Args:
        data: 2D array-like data (e.g., raster grid).
        coordinates: Tuple (x, y) representing coordinate arrays or extent [xmin, xmax, ymin, ymax].
        title: Title of the plot.
        cmap: Colormap to use.
        figsize: Figure size tuple.

    Returns:
        Matplotlib figure and axis objects.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # If coordinates are provided as an extent [xmin, xmax, ymin, ymax]
    if isinstance(coordinates, (list, tuple)) and len(coordinates) == 4:
        extent = coordinates
    else:
        # Otherwise assume coordinates are arrays and derive the extent
        x, y = coordinates
        extent = [np.min(x), np.max(x), np.min(y), np.max(y)]
    
    img = ax.imshow(data, extent=extent, origin='upper', cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.colorbar(img, ax=ax, label="Value")
    plt.tight_layout()
    return fig, ax

def plot_composite_index(time, indices, labels, title="Composite Drought Indices", xlabel="Time", ylabel="Index Value", figsize=(10, 6)):
    """
    Plot multiple drought indices on a single time series plot.

    Args:
        time: Array-like of datetime objects or indices.
        indices: List of array-like or Pandas Series, each representing an index.
        labels: List of labels for each index.
        title: Title of the plot.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        figsize: Figure size tuple.

    Returns:
        Matplotlib figure and axis objects.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    for data, label in zip(indices, labels):
        ax.plot(time, data, label=label, marker='o', linestyle='-')
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    return fig, ax
