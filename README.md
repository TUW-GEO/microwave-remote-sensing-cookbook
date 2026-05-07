```{image} https://gitlab.tuwien.ac.at/cookbooks/templates/tu-cookbook-config/-/raw/main/logos/TU_Logo.png
:width: 50%
:align: left
```

# Microwave Remote Sensing Cookbook

[![nightly-build](https://gitlab.tuwien.ac.at/cookbooks/private/microwave_remote_sensing_cookbook/badges/main/pipeline.svg?key_text=nightly&key_width=50)](https://gitlab.tuwien.ac.at/cookbooks/templates/microwave_remote_sensing_cookbook//-/commits/main)
[![Binder](https://binder.cookbooks.datalab.tuwien.ac.at/badge_logo.svg)](https://binder.cookbooks.datalab.tuwien.ac.at/v2/gl/cookbooks%2Fprivate%2Fmicrowave_remote_sensing_cookbook/HEAD)

This TU Cookbook provides comprehensive, interactive notebooks for learning microwave remote sensing with Synthetic Aperture Radar (SAR) data. Designed for university courses on Microwave Remote Sensing, it guides students through the complete workflow of SAR data processing—from data discovery and preprocessing to advanced analysis techniques like interferometry and phase unwrapping.

The notebooks use real-world data from Sentinel-1 and ALOS-2 satellites, covering both C-band and L-band SAR systems. Students will gain hands-on experience with Python libraries for geospatial analysis, including pystac for data discovery, xarray for multi-dimensional array handling, and specialized tools for SAR processing.

## Motivation

Microwave remote sensing is an essential tool for Earth observation, providing全天候 monitoring capabilities and unique insights into surface properties, vegetation structure, soil moisture, and ground deformation. This cookbook was developed to bridge the gap between theoretical knowledge and practical application of SAR processing techniques.

The materials are designed to help students develop practical skills in SAR data analysis, enabling them to work independently with complex remote sensing data and apply these techniques to real-world research questions in fields such as:
- Land cover and land use mapping
- Vegetation monitoring and agricultural applications
- Surface deformation and natural hazard monitoring
- Soil moisture estimation
- Disaster response and assessment

## Authors

TU Cookbook Development Team.

## Structure

The cookbook is organized into 9 in-class exercise notebooks with corresponding homework assignments, covering the following topics:

**Notebook 1: Discover and Read SAR Data**
Learn to access radar data using SpatioTemporal Asset Catalog (STAC), query the EODC catalog for Sentinel-1 data, explore metadata, and load data into analysis-ready formats.

**Notebook 2: Unit Conversion**
Understand the critical importance of converting between decibel (dB) and linear scales for SAR backscatter data, with practical examples of when and why each scale is appropriate.

**Notebook 3: Backscattering Coefficients**
Explore different backscatter coefficients (σ⁰, γ⁰), geometric terrain correction, radiometric terrain correction, and their impact on SAR imagery interpretation.

**Notebook 4: Datacubes**
Master the creation and manipulation of spatiotemporal datacubes by stacking multiple SAR products, comparing different sensors, and performing reprojection operations.

**Notebook 5: Wavelength and Polarization**
Compare C-band and L-band SAR responses across different land cover types, analyze co-polarization vs cross-polarization, and examine relationships with vegetation indices.

**Notebook 6: Dielectric Properties**
Analyze backscatter signatures for different land surfaces (water, forests, grasslands, urban areas) and integrate with CORINE Land Cover data for classification and analysis.

**Notebook 7: Speckle Statistics**
Understand speckle noise in SAR imagery, implement spatial filtering (Lee filter) and temporal filtering techniques to reduce speckle while preserving image information.

**Notebook 8: Interferograms**
Learn SAR interferometry for measuring ground deformation using Single Look Complex (SLC) data, including coregistration, coherence estimation, and topographic phase removal.

**Notebook 9: Phase Unwrapping**
Master phase unwrapping techniques to extract continuous phase information from interferograms, apply displacement calculations, and analyze deformation patterns.

Each notebook includes executable code cells, explanatory text, interactive visualizations, and exercises to reinforce learning. The homework assignments provide opportunities for students to practice and extend the concepts introduced in class sessions.

## Running the Notebooks

### Running on dataLAB JupyterHub

Go to the website dataLAB: https://hub.jaas.datalab.tuwien.ac.at

### Running on dataLAB Binder

### Running on Your Own Machine

If you are interested in running this material locally on your computer, you will
need to follow this workflow:

1. Clone the `https://gitlab.tuwien.ac.at/cookbooks/public/microwave_remote_sensing_cookbook` repository:

   ```bash
    git clone https://gitlab.tuwien.ac.at/cookbooks/microwave_remote_sensing_cookbook
   ```

2. Move into the `microwave_remote_sensing_cookbook` directory
   ```bash
   cd microwave_remote_sensing_cookbook
   ```

3. Create a virtual environment with all the required libraries and dependencies
   For that a couple of Options are available:
   - uv
   - conda
   - Docker

#### uv

Create and activate your virtual environment
   ```bash
   uv sync --all-extras
   ```
Start up Jupyterlab Server in the notebooks directory
   ```bash
   uv run jupyter lab notebooks/
   ```

#### Conda

Create and activate your conda environment from the `environment.yml` file
   ```bash
   conda env create -f environment.yml
   conda activate tucookbooks
   ```
Move into the `notebooks` directory and start up Jupyterlab
   ```bash
   jupyter lab notebooks/
   ```

#### Docker

When available simply run `docker compose` to start a Jupyter Lab instance.

1. Start Jupyter Lab from a Docker container:

   ```bash
   docker compose up
   ```
2. Copy Jupyter Lab URL to web browser:

Stop and remove the container

1. Stop Docker container with `CTRL + C`

2. Remove container:

   ```bash
   docker compose down
   ```
