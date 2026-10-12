set windows-shell := ["powershell"]

# Load JHUB_REGISTRY_USER/JHUB_REGISTRY_PASSWORD (and other vars) from .env
set dotenv-load := true

# Default command lists all available recipes
[default]
_default:
    @just --list

alias c := clean
alias d := docs
alias h := hooks
alias i := info
alias l := lint
alias q := check
alias t := test
alias fmt := format

# display the system/project information
[group("chore")]
info:
    @echo "{{ CYAN }}Arch{{ NORMAL }}: {{ arch() }}"
    @echo "{{ CYAN }}OS{{ NORMAL }}: {{ os_family() }}, {{ os() }}"
    @echo "{{ CYAN }}Num CPU's{{ NORMAL }}: {{ num_cpus() }}"
    @echo "{{ CYAN }}Project{{ NORMAL }}: `uv version`"

# run the linter [arg:<full|concise|...>]
[group("style")]
lint arg="concise":
    uv run ruff check . --fix --output-format={{ arg }}

# run the formatter
[group("style")]
format:
    uv run ruff format .

# run the type checker [arg:<full|concise|...>]
[group("style")]
types arg="concise":
    uv run ty check --output-format={{ arg }}

# lint, format and type-check [arg:<full|concise|...>]
[group("style")]
check arg="concise":
    -@just lint {{ arg }}
    -@just format
    -@just types {{ arg }}

# run the tests
[group("test")]
test *args:
    uv run pytest {{ args }}

# run the tests in different Python versions
[group("test")]
testall *args:
    uv run --python=3.12 pytest {{ args }}
    uv run --python=3.13 pytest {{ args }}

# run the formatter, linter, typechecker and the tests
[group("test")]
ci python="3.12":
    uv run --python={{ python }} ruff format .
    uv run --python={{ python }} ruff check . --fix
    uv run --python={{ python }} ty check .
    uv run --python={{ python }} pytest

# install the pre-commit hooks
[group("dev")]
hooks:
    uvx prek install

# clean all build/compilation files and directories
[group("dev")]
clean: clean-build clean-pyc clean-test

# remove build artifacts
[private]
clean-build:
    rm -fr build/
    rm -fr _build/
    rm -fr dist/
    rm -fr .eggs/
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -f {} +

# remove Python file artifacts
[private]
clean-pyc:
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +

# remove test and coverage artifacts
[private]
clean-test:
    rm -f .coverage
    rm -fr htmlcov/
    rm -fr .pytest_cache

# install dependencies in local venv
[group("dev")]
venv:
    uv sync --all-groups --all-extras

# update dependencies in the lock file
[group("dev")]
update:
    uv lock --upgrade

# build the source distribution and wheel file
[group("dev")]
dist:
    uv build

# serve the documentation on localhost
[group("dev")]
docs *args="--execute": venv
    yes | uv run myst start {{ args }}

_ensure_clean:
    @git diff --quiet
    @git diff --cached --quiet

_set_version target:
    case "{{ target }}" in \
        [0-9]*.[0-9]*.[0-9]*) \
            uv version {{ target }} ;; \
        *) \
            uv version --bump {{ target }} ;; \
    esac
    uv lock

# initialize a new git repository
[group("chore")]
init: venv
    git init --initial-branch=main
    git add .
    git commit -m "initial commit"
    @echo "{{ GREEN }}{{ BOLD }}Git has been initialized{{ NORMAL }}"

# write the changelog from commit messages (gh:pawamoy/git-changelog)
[group("chore")]
changelog version=`uv version --short`:
    uvx git-changelog -Tio CHANGELOG.md -B="{{ version }}" -c conventional

_commit_and_tag version=`uv version --short`:
    git add pyproject.toml uv.lock CHANGELOG.md
    git commit -m "chore(release): bumped version to {{ version }}"
    git tag -a "v{{ version }}"

# make a new release [target:<major|minor|patch|...> or semver]
[group("chore")]
release target: test
    @just _ensure_clean
    @just _set_version {{ target }}
    @just changelog
    @just _commit_and_tag
    @echo "{{ GREEN }}Release complete. Run 'git push && git push --tags'.{{ NORMAL }}"

# create a new notbook from a template
[group("chore")]
new *args:
    uv run tu-cookbook new {{ args }}

# validate that the Harbor credentials are available
# (loaded from .env via `set dotenv-load` at the top of the Justfile)
[private]
_authentication:
    #!/usr/bin/env bash
    set -euo pipefail
    : "${JHUB_REGISTRY_USER:?JHUB_REGISTRY_USER is not set (add it to .env or export it)}"
    : "${JHUB_REGISTRY_PASSWORD:?JHUB_REGISTRY_PASSWORD is not set (add it to .env or export it)}"

# build the Image and push it to the DataLab Harbor registry
# (mirrors the jhub-image job in .gitlab-ci.yml)
# Uses docker locally (a rootful daemon handles the jupyter base image's USER/chown
# steps without user-namespace issues). CI uses buildah; see .gitlab-ci.yml.
[group("build")]
jhub-image registry="registry.datalab.tuwien.ac.at" namespace="tuw-geo" repo="microwave-remote-sensing-cookbook" dockerfile="Dockerfile.jhub" tag="latest": (_authentication)
    #!/usr/bin/env bash
    set -euo pipefail
    docker login -u "$JHUB_REGISTRY_USER" -p "$JHUB_REGISTRY_PASSWORD" "{{ registry }}"
    docker build -f "{{ dockerfile }}" -t "{{ registry }}/{{ namespace }}/{{ repo }}:{{ tag }}" .
    docker images
    docker push "{{ registry }}/{{ namespace }}/{{ repo }}:{{ tag }}"
