"""Make URLs for Intake catalog and geotiffs.

Returns
-------
        URL for intake catalog : str
        URL for Sentinel-1 and Alos-2 geotiff : str

"""

import os
import urllib.parse
from enum import StrEnum  # type: ignore[unresolved-import]
from pathlib import Path

import gitlab
import s3fs
from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color
from typing_extensions import TypedDict

ROOT = "https://gitlab.tuwien.ac.at"
REPO_API = "api/v4/projects/1264/repository/files"
REPO_RAW = "cookbooks/data/microwave-remote-sensing-cookbook/-/raw"

S3_ENDPOINT = "https://s3.garage.staging.jaas.datalab.tuwien.ac.at"
S3_BUCKET = "cookbook-microwave-remote-sensing"

os.environ["CACHE_DEST"] = str(
    Path(
        "~/shared/datasets/geo/sync/courses/120.030_Microwave-Remote-Sensing",
    ).expanduser(),
)


class _SensorOptions(StrEnum):
    """Supported Sensor Options."""

    ALOS2 = "alos-2"
    SENTINEL1 = "sentinel-1"


class _CorineColorMapping(TypedDict):
    """Data Model of the expected Corine Color Mapping."""

    value: int
    color: Color
    label: str


class CorineColorCollection(BaseModel):
    """Data Model of the expected Corine Color Mapping Collection."""

    items: list[_CorineColorMapping] = Field(alias="land_cover")

    def to_dict(self) -> dict[int, _CorineColorMapping]:
        """Convert to dictionary."""
        return {item["value"]: item for item in self.items}


def get_intake_url(
    root: str = ROOT,
    branch: str = "main",
    repo: str = REPO_RAW,
    notebook: int | None = None,
    *,
    verbose: bool = True,
) -> str:
    """Create URL for an intake catalog.

    Parameters
    ----------
    root : str
        Root of URL
    branch: str
        The branch from the repo that should be accessed
    repo: str
        The repo that the intake should take the data from
    notebook: int | None
        Optional notebook number (3-9). When provided, points at the
        per-notebook catalog ``microwave-remote-sensing-<N>.yml``; otherwise
        the combined ``microwave-remote-sensing.yml``.
    verbose: bool
        If true prints the returned path to stdout

    Returns
    -------
        Intake catalog : str

    """
    catalog_name = (
        f"microwave-remote-sensing-{notebook}.yml"
        if notebook is not None
        else "microwave-remote-sensing.yml"
    )
    intake_path = f"{root}/{repo}/{branch}/{catalog_name}"
    if verbose:
        print(intake_path)
    return intake_path


def make_gitlab_urls(sensor: _SensorOptions | str) -> list[str]:
    """Create URL to Alos and Sentinel filed on GitLab.

    Parameters
    ----------
    sensor : str
        either "alos-2" or "sentinel-1"

    Returns
    -------
        URL : list[str]

    """
    gl = gitlab.Gitlab(url=ROOT)
    gl_project = gl.projects.get(id=1264)
    root = f"{ROOT}/{REPO_API}/"
    end = "/raw?ref=main&lfs=true"
    return [
        root + urllib.parse.quote_plus(gitlab_file["path"]) + end
        for gitlab_file in gl_project.repository_tree(
            path=sensor,
            ref="main",
            recursive=True,
            iterator=True,
        )
        if gitlab_file["path"].endswith(".tif")
    ]


def _s3_filesystem() -> "s3fs.S3FileSystem":
    """Create the S3 filesystem for the Garage object storage.

    Credentials are expected in the standard AWS environment variables
    (``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``) and the endpoint is
    configured for the TU Wien Garage deployment.

    Returns
    -------
    s3fs.S3FileSystem
        Configured filesystem for the cookbook bucket.

    """
    return s3fs.S3FileSystem(
        key="GKcbb84001a55544bde09c0872",
        secret="28c2e5fc6ebb6445ccabe16793bbf62631a04b93333d305f54b248a3b07e989d",
        endpoint_url=S3_ENDPOINT,
        client_kwargs={"region_name": "garage"},
    )


def make_s3_urls(sensor: _SensorOptions | str) -> list[object]:
    """Find geotiff files for a sensor on S3 object storage.

    Paths are globbed recursively (``**``) for ``*.tif`` under the sensor
    directory and returned as ``fsspec`` OpenFile objects so they can be
    handed directly to ``xarray.open_mfdataset``.

    Parameters
    ----------
    sensor : str
        either "alos-2" or "sentinel-1"

    Returns
    -------
    list[fsspec.core.OpenFile]
        OpenFile objects for the matching geotiffs.

    """
    fs = _s3_filesystem()
    pattern = f"{S3_BUCKET}/{sensor}/**/*.tif"
    keys = sorted(fs.glob(pattern))
    return [fs.open(f"s3://{key}", "rb") for key in keys]
