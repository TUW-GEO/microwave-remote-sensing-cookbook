---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: Python 3
  name: python3
---

# Homework Exercise 1: Discover Sentinel 1 data using the EODC STAC catalog

+++
## Overview

In the previous notebook, you have learnt how to access Sentinel-1 data from EODC using the STAC API. Your task now is to find and plot a Sentinel-1 acquisition of your latest holiday destination. To successfully finish the exercise, you need to perform the following tasks:

- [ ] Get the 'SENTINEL1_SIG0_20M' collection
- [ ] Define a spatial and temporal extent
- [ ] Perform the STAC request and select one of the resulting items
- [ ] Check the metadata to find the relative orbit number of the item
- [ ] Read and decode the items
- [ ] Plot one of the items

## Imports

To help you to get started, we already imported all required packages and provided some code blocks. Your task is now to fill in the missing code cells indicated with # YOUR CODE HERE.

```{code-cell} ipython3
import pystac_client
from odc import stac as odc_stac
```

## List all collection names and select one

```{code-cell} ipython3
---
tags: [skip-execution]
---
eodc_catalog = pystac_client.Client.open("https://stac.eodc.eu/api/v1")

colllection_id = ...  # YOUR CODE HERE

collection = eodc_catalog.get_collection(colllection_id)
collection
```

## Define spatial and temporal extent and use client to load the metadata

```{code-cell} ipython3
---
tags: [skip-execution]
---
# Define the area of interest by providing coordinates that cover your latest
# holiday destination (can be a city, state, country, etc.)
latmin, latmax = ...  # YOUR CODE HERE
lonmin, lonmax = ...  # YOUR CODE HERE
bounds = (lonmin, latmin, lonmax, latmax)

# Define the time range. This can either be the data of your actual holiday or
# any other time range between 2016 and 2023
time_range = ...  # YOUR CODE HERE

items = ...  # YOUR CODE HERE

print(len(items), "scenes found.")
```

## Find necessary metadata, like bands, resolution, coordinate reference system

```{code-cell} ipython3
---
tags: [skip-execution]
---

# Pick one item from items using indexing get the relative orbit from the item
# properties
relative_orbit = ...  # YOUR CODE HERE
print(f"The relative orbit number of the item is {relative_orbit}")
```

## Lazily load the data into an Xarray

**Take care that your dataset is not to big by limiting the bounds and time range!**

```{code-cell} ipython3
---
tags: [skip-execution]
---

bands = ...  # YOUR CODE HERE
chunks = {"time": 1, "x": 1000, "y": 1000}

sig0_dc = odc_stac.load(
    items,
    bands=bands,
    bbox=bounds,
    chunks=chunks,
)
```

## Define the nodata value and scale factor and decode the data

```{code-cell} ipython3
---
tags: [skip-execution]
---

nodata = ...  # YOUR CODE HERE
scale = ...  # YOUR CODE HERE

sig0_dc = ...  # YOUR CODE HERE
```

## Plot the loaded data

```{code-cell} ipython3
---
tags: [skip-execution]
---

...  # YOUR CODE HERE
```

## Wrapping Up

In this exercise, you practiced:

- Connecting to a STAC catalog and retrieving the Sentinel-1 collection
- Defining search parameters for your specific location and time period
- Extracting metadata items from search results
- Loading backscatter data into a lazily-evaluated xarray DataArray
- Applying proper scaling and NoData handling
- Visualizing SAR data with geospatial context
