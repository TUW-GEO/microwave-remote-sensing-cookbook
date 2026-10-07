FROM quay.io/jupyter/minimal-notebook:latest

USER root

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt-get update && \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -yq --no-install-recommends \
        nodejs jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
           /tmp/* \
           /var/tmp/* \
           /usr/share/doc/* \
           /usr/share/man/* \
           /var/cache/apt/*

USER ${NB_UID}
COPY --chown=${NB_UID}:${NB_GID} . /home/jovyan/microwave_remote_sensing_cookbook
WORKDIR /home/jovyan/microwave_remote_sensing_cookbook

RUN uv sync
ENV PATH="/home/jovyan/microwave_remote_sensing_cookbook/.venv/bin:${PATH}"
RUN uv run python -m ipykernel install --name python3 --display-name "Python 3 (ipykernel)" --user
