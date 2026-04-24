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

# Homework Exercise 4: Datacubes

For the homework assignement we will continue work on the same data as in the in-class exercise. Hence we will load the same data which has been stored as a Zarr datastore. Zarr is efficient for storing chunked data and much faster for reading.

```{code-cell} ipython3
import xarray as xr
import rioxarray  # noqa
from pathlib import Path

import hvplot.xarray  # noqa
import intake

from microwave_remote_sensing_cookbook.catalog import get_intake_url
```

```{code-cell} ipython3
---
tags: skip-execution
---
url = get_intake_url()
cat = intake.open_catalog(url)
fused_ds = cat["fused_array"].read().compute()
fused_ds
```

We want to expand the datacube of the in-class exercise with a new variable in this assignment. The new variable is the Leaf Area Index (LAI), which is a dimensionless index measuring the one-sided green leaf area over a unit of land ($m^2 \cdot m^{-2}$).

## Question 1

Load the new LAI data with the below provided code snippet and extract the CRS and resolution of the raster. Apply what you have learned in the in-class exercise by only using the packages as listed in the imports of this notebook.

```{code-cell} ipython3
---
tags: skip-execution
---
url = get_intake_url()
cat = intake.open_catalog(url)
lai_ds = cat["lai"].read().compute()
lai_ds
```

## Question 2

In order to compare LAI with ALOS-2 L-band and Sentinel-1 C-band data, we will merge this variable with the SAR datacube (of the in-class exercise). Let's first check the temporal range of the SAR datacube (`fused_ds`) and the new `xarray` dataset: `lai_ds`.

```{code-cell} ipython3
---
tags: skip-execution
---
fused_ds.time
```

```{code-cell} ipython3
---
tags: skip-execution
---
lai_ds.time
```

The temporal range of `lai_ds` is longer then the fused ALOS-2 L-band and Sentinel-1 C-band datacube. To fit `lai_ds` object to the SAR datacube, we will need to cut the `lai_ds` temporal extent using the selection method (`sel`). Complete the following code snippet to perform the previous described selection operation.

```{code-cell} ipython3
---
tags: skip-execution
---

lai_ds = ...  # YOUR CODE HERE
lai_ds.time
```

## Question 3

Now that the temporal range of the LAI datacube matches that of `fused_ds`, we can continue by aligning the spatial coordinates, so that we can create a datacube containing both variables (LAI and SAR data). Yet again, apply the same methods as shown in the in-class exercise.

Let's break this down into steps first align both datacubes.

1. Align both datacubes. Remember to use the `rioxarray` package and use the default resampling method.

```{code-cell} ipython3
---
tags: skip-execution
---

lai_ds = ...  # YOUR CODE HERE
lai_ds
```

2. Write the coordinates of `fused_ds` to the reprojected `lai_ds` object to prevent mistakes caused by floating point errors. Use the `assign_coords` method.

```{code-cell} ipython3
---
tags: skip-execution
---

lai_ds = ...  # YOUR CODE HERE
lai_ds
```

If the previous operations were successfull, 3) we can merge the two variables: SAR and LAI. We use a different `xarray` function for this, where we combine the two variable to a `xarray.DataSet` with the `merge` function.

```{code-cell} ipython3
---
tags: skip-execution
---

# YOUR CODE HERE ----------------------------------------------------------
fused_ds = ...  # combine two variables in an Xarray.Dataset
# YOUR CODE HERE ----------------------------------------------------------
fused_ds
```

The last step is the 4) `resample` operation to align the timestamps. Use again a median value.

```{code-cell} ipython3
---
tags: skip-execution
---

fused_ds = ...  # YOUR CODE HERE
```

Plot the LAI variable with the following lines of code to check your results:

```{code-cell} ipython3
---
tags: skip-execution
---

fused_ds.LAI.\
    dropna(dim="time", how="all").\
    hvplot.image(robust=True, data_aspect=1, cmap="viridis", rasterize=True).\
    opts(frame_height=400, aspect="equal")
```

```{code-cell} ipython3
---
tags: skip-execution
---

to_store = fused_ds.copy()
for var in to_store.variables:
    to_store[var].encoding.clear()
to_store.to_zarr("fused_ds.zarr", mode="w")
```
