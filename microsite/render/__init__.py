"""
Module for rendering HTML files from source Markdown files.
"""

import logging
import shutil

from abc import ABC, abstractclassmethod
from microsite import path as ms_path
from microsite.util import AttrDict, Engine
from shutil import rmtree
from pathlib import Path


log = logging.getLogger(__name__)


class RenderEngine(ABC, Engine):
    """Abstract class representing common features of a rendering engine.

    :param name: The name of the rendering engine.
    :type name: str

    :param config: A dict containing operating parameters for this rendering engine.
    :type config: dict

    :param index: Dict where the keys are paths to source files and the values are dicts with
        the following optional settings:

        - ``tags``: List of terms relevant to the content of the page.
        - ``title``: Used to override the ``<title>`` text for the page.
    """

    def __init__(self, name: str, config: AttrDict, index: dict = {}):
        super().__init__(name=name, config=config)
        self.index = index
        log.debug(f'Created rendering engine {name} with options: {config}')
        log.debug(f'Document index: {self.index}')

    @abstractclassmethod
    def render(self, source_dir: str, target_dir: str, paths: list[str]) -> list[str]:
        """
        Abstract function representing a RenderEngine's rendering process.

        :param source_dir: Top-level directory containing source files to render.
        :type source_dir: str | Path

        :param target_dir: Top-level directory to render files into.
        :type target_dir: str | Path

        :param paths: List of all paths in the source directory to be processed. Not every path in
            this list will be rendered.
        :type paths: list[str]
        """
        pass


def render(
    engines: list[RenderEngine],
    source_dir: str,
    target_dir: str,
    delete_target_dir: bool = True,
) -> None:
    """
    Discover all files contained within ``source_dir``. Pass all files into each rendering engine.
    Track whether each file has been altered by one of these rendering processes. Copy any unaltered
    files into the target location directly.

    :param source_dir: The top level directory containing all source files.
    :type source_dir: str

    :param target_dir: The top level directory where all rendered output will be placed. Will be
        created if it does not exist.
    :type target_dir: str

    :param delete_target_dir: When True, if the target directory exists, delete it before building.
        This ensures a clean build environment. Defaults to True.
    :type delete_target_dir: bool, optional

    :raises IOError: When the target directory exists, but you have provided
        ``delete_target_dir=False``.
    :raises ValueError: When the stylesheet's target filename conflicts with a filename in the
        source content.
    """

    # Prepare target directory
    log.debug(f'Preparing target directory: {target_dir}')
    target_path = Path(target_dir)
    if target_path.exists():
        if delete_target_dir:
            log.info('Target directory already exists. Deleting it now to ensure a clean build.')
            rmtree(target_path)
        else:
            raise IOError(
                'Target directory already exists, but project settings specified not to delete it.'
            )

    log.info(f'Creating target directory {target_dir}')
    target_path.mkdir()

    log.debug(f'Rendering the contents of {source_dir} into {target_dir}')
    ms_path.validate_dir(source_dir)
    source_files = ms_path.get_all_paths(source_dir=source_dir)

    log.debug('Found the following files:')
    for file in source_files:
        log.debug(str(file))

    rendered_paths = []
    for engine in engines:
        rendered_paths.extend(
            engine.render(source_dir=source_dir, target_dir=target_dir, paths=source_files)
        )
    # Remove duplicates from the list
    rendered_paths = set(rendered_paths)

    # Determine what was not affected
    missed_paths = [path for path in source_files if path not in rendered_paths]

    for path in missed_paths:
        log.info(f'Copying unrendered file {path}')
        shutil.copy(f'{source_dir}/{path}', f'{target_dir}/{path}')
