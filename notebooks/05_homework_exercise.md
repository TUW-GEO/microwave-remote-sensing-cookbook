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

# Homework Exercise 5: SAR Wavelength and Polarization

## Overview

This homework exercise will test your understanding of:

- Backscatter differences between C-band and L-band
- Co-polarization (VV, HH) vs cross-polarization (VH, HV)
- Using auxiliary data like NDVI to analyze backscatter patterns
## Imports


We have seen that cross- and co-polarized signals for Sentinel-1 and ALOS-2 seem to be dependent on the type of vegetation. Let's have a closer look at this.

```{code-cell} ipython3
import numpy as np
import xarray as xr
import pandas as pd

import holoviews as hv
import hvplot.xarray  # noqa
import intake

from microwave_remote_sensing_cookbook.catalog import get_intake_url

from microwave_remote_sensing_cookbook.mc_widgets import AnswerStore, MCQuestion
```

```{code-cell} ipython3
---
tags: [hide-cell]
jupyter:
  source_hidden: true
---
store = store = AnswerStore("answers.json")

QUESTIONS = {
    "Q2": {
    "a": "a) As a forest gets denser (higher LAI), the strength of the cross-polarized return signal will always increase, regardless of the radar band used.",
    "b": "b) As a forest gets denser (lower LAI), the strength of the cross-polarized return signal will not change, regardless of the radar band used.",
    "c": "c) At high Leaf Area Index, the cross-polarized backscatter returns are stronger at L-band than at C-band wavelengths.",
    "d": "d) The received energy of co-polarized backscattering at high LAI is higher for L-band than for C-band wavelength.",
    },
}
```

## Question 1

We will try to highlight the difference between cross- and co-polarized microwave backscattering for Sentinel-1 and ALOS-2 separately. As already indicated volume scattering leads to depolarization effects, where multiple scattering can cause a change in polarization. Hence, a cross-polarized receiving antenna, such as on-board the Sentinel-1 and ALOS-2 satellites, may receive less energy from smooth bare soils than from vegetated surfaces. And the received energy for a cross-polarized receiving antenna will increase with increasing vegetation density. Hence this property of depolarization with vegetation density can be formulated as the _cross-polarised ratio_.

$r_{cross} = \frac{P_{VH}}{P_{VV}} = \frac{\gamma^0_{VH}}{\gamma^0_{VV}}  \quad \text{for Sentinel-1}$

$r_{cross} = \frac{P_{HV}}{P_{HH}} = \frac{\gamma^0_{HV}}{\gamma^0_{HH}}  \quad \text{for ALOS-2}$

Note that in the literature, this formulation may also appear with the numerator and denominator swapped (i.e., as VV/VH instead of VH/VV), depending on the convention adopted by the authors. In this notebook you will calculate cross-polarised ratios for Sentinel-1 and ALOS-2 as reported in the above equations.

First load again the same dataset.

<div class="alert alert-block alert-info">
<b>Tip:</b> The calculation of the cross-ratio refers to the linear domain
and therefore needs a conversion from dB to linear scale. Checkout Notebook 2 again for the conversion.
</div>

```{code-cell} ipython3
:tags: [skip-execution]

url = get_intake_url()
cat = intake.open_catalog(url)
fused_ds = cat["fused"].read().compute()
fused_ds
```

Calculate the cross-polarised ratios separately for each of the satellites with standard mathematical operations on the fused `xarray` and store the results in two new `xarray` objects. Make sure to transform the cross-polarised ratio (CR) to linear units for easier interpretation (see below for useful tips).

Since the ratio in linear scale is:

$$
\frac{\gamma^0_{VH,\text{linear}}}{\gamma^0_{VV,\text{linear}}}
$$

and the relationship between dB and linear is:

$$
\gamma^0_{\text{dB}} = 10 \log_{10}(\gamma^0_{\text{linear}})
$$

then the VH/VV cross ratio in linear units is:

$$
\frac{\gamma^0_{VH,\text{linear}}}{\gamma^0_{VV,\text{linear}}}
= 10^{\frac{\gamma^0_{VH,\text{dB}} - \gamma^0_{VV,\text{dB}}}{10}}
$$

```{code-cell} ipython3
:tags: [skip-execution]

rcross_da_s1 = ...  # YOUR CODE HERE
rcross_da_alos = ...  # YOUR CODE HERE
```

After you calculate the CR, plot the results with the following code.

```{code-cell} ipython3
:tags: [skip-execution]

LAI_mean = fused_ds.LAI.mean("time")

LAI_image = LAI_mean.hvplot.\
    image(rasterize=True, cmap='viridis', clim=(0, 6)).\
    opts(title="Mean LAI (Selectable)", frame_height=400, aspect="equal")

id_sat = pd.Index(["sentinel", "alos"], name="sat")
rcross_da = xr.concat([rcross_da_s1, rcross_da_alos], id_sat)


def get_timeseries(x, y):
    """
    Callback Function Holoviews

    Parameters
    ----------
    x: float
        numeric value for x selected on LAI map
    y: float
        numeric value for y selected on LAI map
    """

    lai_value = LAI_mean.sel(x=x, y=y, method="nearest").values

    if np.isnan(lai_value):
        select = rcross_da.where(LAI_mean.isnull())
        label = "Water"
    else:
        mask = np.isclose(LAI_mean, lai_value, atol=0.05)
        select = rcross_da.where(mask)
        label = "Mean LAI: " + str(np.round(lai_value, 1))

    time_series = select.to_dataset("sat").\
        median(["x", "y"], skipna=True).\
        hvplot.scatter(ylim=(0, 0.5)).\
        opts(title=label, frame_height=400)

    return time_series


point_stream = hv.streams.SingleTap(source=LAI_image)
time_series = hv.DynamicMap(get_timeseries, streams=[point_stream])
LAI_image + time_series
```

_Figure 1: (Left) Map of MEAN LAI around Lake Garda. The pixel values can be seen by hovering your mouse over it. Clicking on the pixel will generate the timeseries for the associated mean LAI on the right hand-side. (Right) Timeseries of CR for Sentinel-1 and ALOS-2._

## Question 2

Analyse the plot that you created above. Based on what you see, select the correct statements.

```{code-cell} ipython3
:tags: [hide-input]

MCQuestion(store, "ex5", "Q2", QUESTIONS["Q2"]).show()
```

## Question 3

For this question we will create a boxplot to analyse the sensitivity of CR with to changes in LAI. Sensitivity means how high a response is when we change another variable, like LAI in this case. So an increased sensitivity means a higher response for the same increase in LAI. The boxplot uses boxes to illustrate the distributions of binned LAI values. Box limits indicate the range of the central 50% of the data (a.k.a inter quartile range: IQR), with the median value depicted as a central red line. The whisker limits demarcate 1.5 times the distance of the IQR. Values outside of the whiskers are considered outliers. Outliers have been eliminated in this plot to make the plot more readable.

```{code-cell} ipython3
:tags: [skip-execution]

# labels for LAI bins
ranger = [str(x).zfill(1) for x in range(1, 6)]

# fuse LAI and ALOS-2 and Sentinel-1 CR
LAI_df = fused_ds.LAI.to_dataframe()
LAI_df["LAI"] = LAI_df["LAI"].\
    transform(pd.cut, bins=range(6), labels=ranger)
LAI_df["alos"] = rcross_da_alos.to_dataframe()["gam0"]
LAI_df["s1"] = rcross_da_s1.to_dataframe()["gam0"]

# boxplot
ax = LAI_df.plot.box(column=["s1", "alos"], by="LAI",
                               showfliers=False, figsize=(15, 6))
ax[0].set_xlabel(r"$\text{LAI}$ [$m^2 \cdot m^{-2}$]")
ax[0].set_ylabel(r"$\text{CR}$ [$m^2 \cdot m^{-2}$]")
ax[1].set_xlabel(r"$\text{LAI}$ [$m^2 \cdot m^{-2}$]")
ax[1].set_ylabel(r"$\text{CR}$ [$m^2 \cdot m^{-2}$]")
```

_Figure 2: Boxplot for CR of Sentinel-1 and ALOS-2 for binned LAI values_

Analyse the boxplot above. Based on what you see in the plot, can you tell whether the L-band or the C-band sensor have different sensibilities with regards to changes in vegetation? Can you also tell to what type of vegetation each satellite-sensor is most sensitive to? Explain your reasoning in detail.

## Wrapping Up

In this exercise, you explored:

- Comparing backscatter signatures across different microwave frequencies
- Understanding polarization effects on backscatter
- Using indices like NDVI to relate backscatter to vegetation
- Analyzing seasonal patterns in multi-frequency SAR data
