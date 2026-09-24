---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.5
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

# Homework Exercise 7: Speckle Statistics

During the in-class exercise, we learned about the origin of speckles and ways to mitigate it. In this exercise, your task will be to apply a Lee filter (spatial filter) with different kernel sizes to the same study area.

```{code-cell} ipython3
import intake
import numpy as np
import xarray as xr
from pathlib import Path
from scipy.ndimage import uniform_filter  #noqa
import hvplot.xarray  # noqa

from microwave_remote_sensing_cookbook.catalog import get_intake_url
from microwave_remote_sensing_cookbook.mc_widgets import AnswerStore, MCQuestion
```


```{code-cell} ipython3
---
tags: [hide-cell]
jupyter: {source_hidden: true}
---

store = store = AnswerStore("answers.json")

QUESTIONS = {
    "Q3": {
    "larger_kernel_degrades_resolution": "Enlarging the kernel increases the degree of spatial averaging, which effectively degrades the image's spatial resolution by suppressing local detail.",
    "smaller_kernel_more_speckle_removed": "The smaller the kernel size, the more speckle noise is removed.",
    "kernel_size_no_impact": "The choice of the kernel size has no impact on the speckle noise removal.",
    "no_removal_preserves_temporal": "To preserve the temporal resolution of an image, speckle should not be removed.",
    "larger_kernel_more_speckle_removed": "The larger the kernel size, the more speckle noise is removed.",
    "temporal_preferable_to_spatial": "A temporal filtering approach is generally preferable to a purely spatial filtering approach for speckle reduction, even when surface changes are evident across temporal observations of the same scene.",
    },
}
```

## Question 1

+++

## Overview

This homework exercise will test your understanding of:

- Why speckle occurs in SAR imagery
- Different filtering approaches applied to SAR imagery
- How speckle can help characterize physical properties
## Imports


We will use already known data, which consists of Sentinel-1 **sigma naught** $\sigma^0$ images focusing on Lake Neusiedl and the surrounding area, where the CORINE land cover is used for land cover-based visualization and analysis.

```{code-cell} ipython3
url = get_intake_url()
cat = intake.open_catalog(url)
sig0_da = cat.speckle.read().sig0.compute()
sig0_da
```

Let's build up the Lee filter function:

```{code-cell} ipython3
:tags: [skip-execution]

def lee_filter(raster, size=...):
    """
    Parameters:
    raster: ndarray

    size: int

    Returns:
    filtered_image (ndarray): The filtered image with reduced speckle noise
    """

    filtered_image = ...  # YOUR CODE HERE

    return filtered_image
```

## Question 2

+++

Apply your function and compute the Lee filter for at least two different kernel sizes (size number must be odd).

```{code-cell} ipython3
:tags: [skip-execution]

sig0_da.data = ...  # YOUR CODE HERE
```

Plot you results usign the following code:

```{code-cell} ipython3
:tags: [skip-execution]

sig0_da.hvplot.image(
    x="x", y="y", robust=True, data_aspect=1, cmap="Greys_r", rasterize=True
).opts(frame_height=600, framewise=False, aspect="equal")
```

## Question 3

+++

Based on your plotted results, select which of the below statement is correct:

```{code-cell} ipython3
:tags: [hide-input]

MCQuestion(store, "ex7", "Q3", QUESTIONS["Q3"]).show()
```

## Wrapping Up

In this exercise, you learned:

- The origin of speckle in radar interference
- Spatial vs temporal filtering techniques
- Trade-offs in speckle reduction methods
- How speckle relates to target properties
