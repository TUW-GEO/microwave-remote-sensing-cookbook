---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Homework Exercise 6: Dielectric Properties of Natural Media

## RGB Composite

Not only radar reflectivity vary according to different land cover classes. The backscattered signal also depends on the change of the imagined natural media over time. We may want to capture in one single image how different land covers comparably change across the same time range. A way to do achieve that is by generating a RGB composite. But what is a RGB composite? It all comes down to combining three image bands into one picture by setting each band as either Red, Green or Blue channel.

In order to highlight the temporal variability of the backscatter response, we want to select 3 images with maximal distance in time. Therefore we take the first, the middle and the last time available out of the input images available for this exercise. We use RGB coloring where we want to color the first image with Red, the second with Green and the Third with Blue color. When we overlay the images the color will show the differences over time.

```{code-cell} ipython3
import intake
import numpy as np  # noqa
import pandas as pd
import xarray as xr
import rasterio
from pathlib import Path
import matplotlib.pyplot as plt
from functools import partial
from shapely.geometry import box

from microwave_remote_sensing_cookbook.catalog import CorineColorCollection, get_intake_url
```

## Load Sentinel-1 Data

```{code-cell} ipython3
url = get_intake_url()
cat = intake.open_catalog(url)
sig0_da = cat.neusiedler.read().sig0.compute()
```

## Select the Dates of Interest

To create an RGB composite, we need to choose three distinct dates. It's recommended to select dates that are spaced out to capture noticeable changes over time (e.g., first available date, second date as the middle date of the datacube time window, third date as the last availavable date). Pay attention to the season as well, as vegetation and other environmental factors often change significantly throughout the year.

Tips:

- Select your dates from the `sig0_da` object and define them using the numpy `datetime64` data type.
- Use the `sel` method with nearest neighbor (`method=\"nearest\"`) interpolation method to obtain the resulting `sig0_rgb_da` object.
- Do not forget to use the `compute()` method (when you use the `sel` method) to finally load the result into memory.

```{code-cell} ipython3
#| eval: false

# YOUR CODE HERE ----------------------------------------------------------
first = ...  # YOUR CODE HERE
second = ...  # YOUR CODE HERE
third = ...  # YOUR CODE HERE
# YOUR CODE HERE ----------------------------------------------------------

sig0_rgb_da = ... # YOUR CODE HERE
sig0_rgb_da
```

### Map the backscatter to RGB values

To visualize backscatter data in RGB, we need to transform the data into values between 0 and 1 to match it to colors. The first step is to convert the backscattering values into linear scale so we can perform meaningful calculations. Now we can normalise the values to be between 0 and 1 using the following formula:

$$
sig0_{norm} = \frac{sig0 - sig0_{min}}{sig0_{98th} - sig0_{min}}
$$

We replaced the traditional maximum value with the 98th quantile in our normalization process to enhance robustness against outliers. Due to the nature of backscattering some sigma nought values get very high so taking the 98th quantile is important. The linear backscattering values are bounded by 0 so using for example the 2nd quantile is not necessary. After applying the formula, any values exceeding the 98th quantile will be greater than 1. We map these values to 1 to ensure they fit within our specified range."

```{code-cell} ipython3
#| eval: false

linear_ds = 10 ** (sig0_rgb_da / 10)

min_value = linear_ds.quantile(0.02).item()
max_robust = linear_ds.quantile(0.98).item()


def normalize(val, min, max):
    """
    Min-max normalize value

    Parameters
    ----------
    val: float
        target
    min: float
        minimum value of range
    max: float
        maximum value of range
    Returns
    -------
    float
    """

    return (val - min) / (max - min)


normalized_ds = normalize(linear_ds, min_value, max_robust).clip(min=0, max=1)

fig, ax = plt.subplots(figsize=(8, 5))
normalized_ds.isel(time=0).plot().axes.set_aspect("equal")
plt.tight_layout()
```

## Individual RGB Channels

Let´s first plot the three normalized images separately (Red = Oldest image, Green = Middle image, Blue = Newest image).

```{code-cell} ipython3
#| eval: false

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

normalized_ds.isel(time=0).plot(ax=axes[0], cmap="Reds")
normalized_ds.isel(time=1).plot(ax=axes[1], cmap="Greens")
normalized_ds.isel(time=2).plot(ax=axes[2], cmap="Blues")

axes[0].set_aspect("equal")
axes[1].set_aspect("equal")
axes[2].set_aspect("equal")

plt.tight_layout()
```

## Plotting the RGB Composite

And finally, let´s plot the RGB composite.

```{code-cell} ipython3
#| eval: false

fig, ax = plt.subplots(figsize=(8, 5))

normalized_ds.plot.imshow()
ax.set_aspect('equal')

plt.tight_layout()
```

## Question

What can you infer about the landscape features (focus on the crops appearance, forested areas, water bodies, urban areas) based on the variations in color across the image? Describe how you might interpret the colors in terms of changes over time, surface properties, and dielectric properties of the natural and artificial media.
Focus on the crops: keeping in mind the polarization of the visualized backscatter data (i.e., VV) and its sensitivity to smoother surfaces (which indicates lack of vegetation), what does the blue color represent?
