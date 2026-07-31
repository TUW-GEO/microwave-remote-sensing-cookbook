FROM registry.datalab.tuwien.ac.at/jaas/base-notebook:latest

USER root

RUN apt-get update && \
    apt-get install -yq --no-install-recommends git build-essential jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

USER ${NB_UID}
COPY --chown=1000:1000 .. /home/jovyan/microwave_remote_sensing_cookbook
WORKDIR /home/jovyan/microwave_remote_sensing_cookbook

RUN uv export --format requirements.txt --extra book --group dev > requirements.txt
RUN uv pip install -r requirements.txt --system

# Badges live in source for the repo browser + Pages site, but must not appear
# inside the Binder image. turecipe (a [book] extra dependency) provides both
# console scripts. badgeclean strips [![Binder](...)](...) from README +
# notebooks; prune-for-binder drops everything the image does not need to run
# notebooks (allowlist: notebooks/, src/, images/, pyproject.toml,
# environment.yml, myst.yml).
RUN badgeclean && prune-for-binder
