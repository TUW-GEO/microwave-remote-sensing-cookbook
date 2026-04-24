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

# Homework Exercise 3: Backscattering Coefficients

To successfully finish this notebook, you have to answer/solve the following three questions.

```{code-cell} ipython3
import xarray as xr

import matplotlib.pyplot as plt  # noqa
import hvplot.xarray  # noqa
import intake

from pathlib import Path
from functools import partial
from microwave_remote_sensing_cookbook.catalog import get_intake_url
```

```{code-cell} ipython3
url = get_intake_url()
cat = intake.open_catalog(url)
ex3_dc = cat["ex3"].read().compute()
ex3_dc
```

## Question 1

+++

Execute the lines below to create the plot. You now see a SAR image with unknown processing level. Based on what you see, which pre-processing steps have been applied to the image?

- [ ] Cloud masking
- [ ] Geometric terrain correction
- [ ] Conversion to dB
- [ ] Radiometric terrain correction (terrain flattening)

Select the answers you think are correct by editing the markdown text and putting an 'x' in the brackets. Note: One, several, or all answers are possible.

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
---
tags: skip-execution
---

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
