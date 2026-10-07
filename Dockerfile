FROM quay.io/jupyter/minimal-notebook:latest

USER root

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chown=1000:1000 . /home/jovyan/microwave_remote_sensing_cookbook
WORKDIR /home/jovyan/microwave_remote_sensing_cookbook

RUN uv sync
ENV PATH="/home/jovyan/microwave_remote_sensing_cookbook/.venv/bin:${PATH}"
RUN uv run python -m ipykernel install --name python3 --display-name "Python 3 (ipykernel)" --user
