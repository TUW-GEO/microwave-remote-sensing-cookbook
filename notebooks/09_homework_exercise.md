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

# Homework Exercise 9: Phase Unwrapping Exercise

## Overview

This homework exercise will test your understanding of:

- Phase unwrapping concepts and algorithms
- Using unwrapped phase to derive displacement
- Understanding the challenges in large displacement events
## Imports


Your task in this exercise is to read the provided data, plot it, unwrap and plot the phase, and calculate the displacement. Then interpret your results.
The following data were acquired from Sentinel-1 on April 23, 2018, from 16:15:24 to 16:15:51 over the region of Hawaii (same data as 08_homework_exercise).

```{code-cell} ipython3
import cmcrameri as cmc  # noqa: F401
import intake
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import xarray as xr

from microwave_remote_sensing_cookbook.catalog import get_intake_url
from microwave_remote_sensing_cookbook.processing import unwrap_array  # noqa: F401
```

```{code-cell} ipython3
---
tags: skip-execution
---

url = get_intake_url(notebook=9)
cat = intake.open_catalog(url)
ds = cat.ex9.read().compute()


# Set cyclic and linear colormaps
cmap_cyc = sns.color_palette("hls", as_cmap=True)
cmap_lin = "cmc.roma_r"
cmap_disp = "cmc.vik"

# Create a mask for the areas which have no data
mask = (ds.phase != 0).astype(bool)
```

```{code-cell} ipython3
---
tags: skip-execution
---

def compute_complex_band(phase_band, intensity_band):
    """
    Computes the complex-valued band for SAR interferograms from phase and intensity bands.

    Parameters:
    - phase_band (numpy.ndarray): Phase band in radians.
    - intensity_band (numpy.ndarray): Intensity band (magnitude).

    Returns:
    - numpy.ndarray: Complex-valued band with dtype complex128.
    """
    real_part = intensity_band * np.cos(phase_band)
    imag_part = intensity_band * np.sin(phase_band)
    complex_band = real_part + 1j * imag_part
    return complex_band


ds["cmplx"] = compute_complex_band(ds["phase"], ds["intensity"])
ds
```

## Question 1

Plot the above provided data. Please note that we are plotting images in Slant Range geometry (East-West flipped due to the descending acquisition pass).

```{code-cell} ipython3
---
tags: skip-execution
---


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
ds.phase.where(mask).plot.imshow(cmap=cmap_cyc, ax=axes[0]).axes.set_title("Phase")
# YOUR CODE HERE -> (Plot intensity map)
# YOUR CODE HERE -> (Plot coherence map)
plt.tight_layout()
```

## Question 2

Use the above function to unwrap the given interferogram and to plot your result.
Use a coherence threshold of 0.2 for your unwrapping and use the provided lines of code below to coarsen the input (to fasten the process).
Kernels with values higher than 3 might lead the unwrapping function to crash, therefore please do not change it.
It might take up to 1 or 2 minutes to execute the function, let the code run, and the output be printed (it will be cleared out at the end).

```{code-cell} ipython3
---
tags: skip-execution
---
# coarsen
kernel = 3
ds = ds.coarsen(x=kernel, y=kernel, boundary="trim").mean()
```

```{code-cell} ipython3
---
tags: skip-execution
---


unwrapped = ...  # YOUR CODE HERE -> perform unwrapping function

unwrapped.plot.imshow(cmap=cmap_cyc)
```

```{code-cell} ipython3
def displacement(unwrapped: xr.DataArray, lambda_val: float = 0.056) -> xr.DataArray:
    """Calculate the displacement from the unwrapped phase.

    Parameters
    ----------
    unwrapped : xr.DataArray
        Array of the unwrapped phase.
    lambda_val : float, optional
        Wavelength of the radar signal, by default 0.056

    Returns
    -------
    xr.DataArray
        Array of the displacement.

    """
    return unwrapped * -lambda_val / (4 * np.pi)
```

## Question 3

Use the above function to calculate the displacement from the unwrapped interferogram, then plot your result with the correct colormap.
Can you guess which kind of phenomenon is responsible for the ground surface displacement that you observe? Elaborate on the direction of the displacement movement (is it towards or away from satellite?)

```{code-cell} ipython3
# YOUR CODE HERE -> perform displacement function
# YOUR CODE HERE -> plot displacement map
```

## Wrapping Up

In this exercise, you explored:

- The need for phase unwrapping in interferometry
- Statistical approaches to unwrapping
- Calculating LOS displacement from phase
- Limitations of unwrapping in large deformation events
