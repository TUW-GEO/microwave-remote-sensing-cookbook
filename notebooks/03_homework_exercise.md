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

# Homework Exercise 3: Backscattering Coefficients

## Overview

To successfully finish this notebook, you have to answer/solve the following three questions.

## Imports

```{code-cell} ipython3
import xarray as xr

import matplotlib.pyplot as plt  # noqa
import hvplot.xarray  # noqa
import intake

from pathlib import Path
from functools import partial
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
    "Q1": {
        "cloud_masking": "Cloud masking",
        "geometric_terrain_correction": "Geometric terrain correction",
        "conversion_to_db": "Conversion to dB",
        "radiometric_terrain_correction": "Radiometric terrain correction (terrain flattening)",
    },
}

```

```{code-cell} ipython3
url = get_intake_url()
cat = intake.open_catalog(url)
ex3_dc = cat["ex3"].read().compute()
ex3_dc
```

## Question 1

+++

Execute the lines below to create the plot. You now see a SAR image with unknown processing level. Based on what you see, which pre-processing steps have been applied to the image? Note: One, several, or all answers are possible.

```{code-cell} ipython3
:tags: [hide-input]

MCQuestion(store, "ex3", "Q1", QUESTIONS["Q1"]).show()
```

```{code-cell} ipython3
ex3_dc.hvplot.image(
    x="x",
    y="y",
    robust=True,
    data_aspect=1,
    cmap="Greys_r",
    groupby="band",
    rasterize=True,
).opts(frame_height=600, framewise=False, aspect="equal")
```

## Question 2

Name all types of geometric radar image distortions in a SAR image. How are they caused, and how can we get rid of them?

`Your answer here`

+++

## Question 3

Use the figure below question 1 to identify areas that are affected by foreshortening and radar shadows. Use the mouseover to retrieve their x/y coordinates. Then use these coordinates to annotate the following `matplotlib` figure with labels by putting them in the lines indicated with # Your coordinates here.

```{code-cell} ipython3
:tags: [skip-execution]

zoom = ex3_dc.sel(x=slice(11.25, 11.5), y=slice(47.75, 47.5)).band_data
fig, ax = plt.subplots(figsize=(10, 8))

bbox = dict(boxstyle="round", fc="0.8")

ax.annotate(
    "foreshortening",
    xy=(..., ...),  # Your foreshortening coordinates here
    xytext=(0.3, 0.25),
    textcoords="subfigure fraction",
    bbox=bbox,
    arrowprops=dict(facecolor="white", shrink=0.05),
)
ax.annotate(
    "shadows",
    xy=(..., ...),  # Your radar shadow coordinates here
    xytext=(0.47, 0.8),
    textcoords="subfigure fraction",
    bbox=bbox,
    arrowprops=dict(facecolor="white", shrink=0.05),
)

zoom.sel(band="unknown1").plot(robust=True, cmap="Greys_r")
```

## Wrapping Up

In this exercise, you learned:

- The processing steps from GRD to terrain-corrected backscatter
- Identifying geometric distortions like foreshortening in SAR imagery
- Understanding the differences between backscatter coefficients
- The impact of terrain correction on backscatter values
