"""Intake reader for S3-hosted JSON files.

This mirrors :mod:`microwave_remote_sensing_cookbook.io.catalog` from the
``data`` cookbook so that the reader class referenced by the generated intake
catalog is resolvable at the same import path in the (binder) reading
environment.
"""

import intake


class S3FilesReader(intake.readers.readers.OpenFilesReader):
    """OpenFilesReader that flattens storage_options for newer s3fs versions.

    In fsspec/s3fs 2026.9.0+, passing ``storage_options=`` as a nested dict to
    ``fsspec.open_files`` misplaces the S3 credentials (they end up under
    ``filesystem.kwargs["storage_options"]`` instead of being attached to the
    filesystem), which breaks session creation. Instead we split the storage
    options into top-level kwargs so they map to ``S3FileSystem``.
    """

    def _read(self, data, **kw):
        kw[self.url_arg] = data.url
        if data.storage_options:
            # Flatten storage options into top-level kwargs for this s3fs version
            kw.update(data.storage_options)
        return self._func(**kw)
