FROM registry.datalab.tuwien.ac.at/cookbooks/tu-cookbook-base-image:0.0.1

COPY --chown=1000:1000 .. /home/jovyan/microwave_remote_sensing_cookbook
WORKDIR /home/jovyan/microwave_remote_sensing_cookbook

RUN uv pip install .[book] ruff ty --system
