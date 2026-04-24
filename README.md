```{image} https://gitlab.tuwien.ac.at/cookbooks/templates/tu-cookbook-config/-/raw/main/logos/TU_Logo.png
:width: 50%
:align: left
```

# TU Cookbook - Microwave Remote Sensing Cookbook

[![nightly-build](https://gitlab.tuwien.ac.at/cookbooks/private/microwave_remote_sensing_cookbook/badges/main/pipeline.svg?key_text=nightly&key_width=50)](https://gitlab.tuwien.ac.at/cookbooks/templates/microwave_remote_sensing_cookbook//-/commits/main)
[![Binder](https://binder.cookbooks.datalab.tuwien.ac.at/badge_logo.svg)](https://binder.cookbooks.datalab.tuwien.ac.at/v2/gl/cookbooks%2Fprivate%2Fmicrowave_remote_sensing_cookbook/HEAD)

Introduce your book here.

## Motivation

Motivation for developing this TU Cookbook.

## Authors

TU Cookbook Development Team.

## Structure

Discuss the structure of the Cookbook.

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
