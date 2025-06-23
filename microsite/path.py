import logging

from pathlib import Path

log = logging.getLogger(__name__)


def get_all_paths(source_dir: str | Path, top_dir: str = None) -> list[str]:
    """
    Returns all paths contained within the source directory. All paths in the returned list of paths are relative to the
    ``top_dir`` set in the initial call to this function. By default (and in basically every real use case), you should
    not specify a ``top_dir``. This causes the ``top_dir`` to be the ``source_dir`` and all returned paths to be
    relative to the ``source_dir``.

    Because this function is recursive and acts on its own findings, it would be mostly redundant to call
    :py:meth:`validate_dir` on each execution of this function. **It is assumed that ``source_dir`` has already been
    validated.**

    :param source_dir: Path to the directory to list.
    :type source_dir: str | Path
    """

    # Determine source and top path
    source_dir = Path(source_dir)  # Even if source_dir is already a Path, this silently succeeds
    if not top_dir:
        top_dir = source_dir
    log.debug(f'Looking for files in {source_dir}')

    # Start with all non-directory files
    all_paths = [path for path in source_dir.iterdir() if path.is_file()]

    # Then expand on each subdirectory recursively
    for path in [path for path in source_dir.iterdir() if path.is_dir()]:
        all_paths.extend(get_all_paths(path, top_dir=top_dir))

    # Convert each path to a string and remove the common top path
    return [str(path).replace(f'{str(top_dir)}/', '') for path in all_paths]


def validate_dir(dir: str) -> bool:
    """
    Returns True if the given path exists, is a directory, and can be accessed.

    :param dir: Path to validate as a directory.
    :type dir: str

    :raises ValueError: Raised if the given path does not exist, is not a directory, or cannot be accessed.

    :return: True if the given path exists
    :rtype: bool
    """

    source = Path(dir).resolve()
    if not source.exists():
        raise ValueError(f'Source directory {source} does not exist.')
    if not source.is_dir():
        raise ValueError(f'Source {source} is not a directory')
    source.stat()
    return True
