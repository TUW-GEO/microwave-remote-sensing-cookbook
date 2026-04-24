---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: microwave-remote-sensing
  language: python
  name: microwave-remote-sensing
---

# Homework Exercise 2: Unit conversion

+++

Your task in this notebook is to load some data from `EODC` and create weekly mosaics across the whole year (the area can be relatively small), plot one of the weekly mosaics, and save it to a file. To successfully finish the exercise, you need to perform the following tasks:

- [ ] Load the data
- [ ] Create weekly mosaics
- [ ] Plot one of the weekly mosaics
- [ ] Save it as a GeoTIFF

As a reminder, backscatter data is typically provided in 'dB', so make sure to perform the mean calculation for the weekly mosaics in the correct domain.

## Load the data

```{code-cell} ipython3
import pystac_client
import odc.stac
from rasterio.crs import CRS
import rioxarray  # noqa
```

```{code-cell} ipython3
#| eval: false

# Search for some data
crs = CRS.from_epsg(27704)  # WGS 84

# Set Spatial extent
latmin, latmax = (
    ...,
    ...,
)
# YOUR CODE HERE, you can choose any location that you like e.g. a city in
# Austria
lonmin, lonmax = ..., ...  # YOUR CODE HERE
bounds = (lonmin, latmin, lonmax, latmax)

# Set Temporal extent
time_range = ...  # YOUR CODE HERE

# Search for Sentinel-1 data
items = (
    pystac_client.Client.open("https://stac.eodc.eu/api/v1")
    .search(
        bbox=bounds,
        collections=["SENTINEL1_SIG0_20M"],
        datetime=time_range,
        limit=100,
    )
    .item_collection()
)

print(len(items), "scenes found")
```

```{code-cell} ipython3
#| eval: false

# Load the data and lazily combine items
sig0_dc = odc.stac.stac_load(
    items,
    bbox=bounds,
    bands=["VV"],
    chunks={"time": 1, "x": 1000, "y": 1000},
)
```

## Preprocess the Data

```{code-cell} ipython3
#| eval: false

# Define the nodata value and scale factor
nodata = -9999  # Sentinel-1 nodata value as defined by EODC
scale = 10  # Sentinel-1 scale factor as defined by EODC

# Preprocess the data
sig0 = ...  # YOUR CODE HERE
```

## Create Weekly Mosaics

```{code-cell} ipython3
#| eval: false

sig0_weekly = ...  # YOUR CODE HERE
```

## Plot one of the Weekly Mosaics

```{code-cell} ipython3
# YOUR CODE HERE
```

## Save one of the Weekly Mosaics as Tif

```{code-cell} ipython3
# YOUR CODE HERE
```
