FROM quay.io/jupyterhub/singleuser:5.5.1@sha256:35cdfffed4de6a8d9393b3157724319e381738c36c7624bd2fca6a6eae99d37d

USER root

COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/

RUN apt-get update && \
    apt-get install -yq --no-install-recommends git build-essential jq && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}
COPY --chown=1000:1000 .. /home/jovyan/microwave_remote_sensing_cookbook
WORKDIR /home/jovyan/microwave_remote_sensing_cookbook

RUN uv pip install .[book] ruff ty --system
