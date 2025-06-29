"""
Module for rendering HTML files from source Markdown files.
"""

import logging
import shutil

from abc import ABC, abstractmethod
from microsite import path as ms_path
from shutil import rmtree
from pathlib import Path


log = logging.getLogger(__name__)


class RenderEngine(ABC):
    def __init__(self, engine: str, config: dict):
        prefix = f'eng_{engine}_'
        engine_opts = {
            key.replace(prefix, ''): value
            for key, value in config.items()
        }
        for key, value in engine_opts.items():
            setattr(self, key, value)
        log.debug(f'Created rendering engine {engine} with options: {engine_opts}')
    
    @abstractmethod
    def render(self, paths: list[str]) -> bool:
        pass


def render(
    engines: list[RenderEngine],
    source_dir: str,
    target_dir: str,
    delete_target_dir: bool = False,
) -> None:
    """
    Discover all files contained within ``source_dir``. Render any Markdown files into HTML files stored in the
    ``target_dir``. Copy any other files directly over.

    :param source_dir: The top level directory containing all source files.
    :type source_dir: str

    :param target_dir: The top level directory where all rendered output will be placed.
    :type target_dir: str

    :param stylesheet: Path to the file containing the CSS to apply to the site.
    :type stylesheet: str

    # :param template: Path to the Jinja2 template to use when rendering HTML. When rendering, this has access to the
    #     "stylesheet" (relative path to the stylesheet to load), "title" (string to display in the tab/title bar), and
    #     "html" (the HTML rendered from the Markdown) variables.
    # :type template: str

    :param delete_target_dir: When True, if the target directory exists, delete it before building. Defaults to False.
    :type delete_target_dir: bool, optional

    # :param markdown_extensions: List of Markdown extensions to enable. See
    #     https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/index.md#officially-supported-extensions
    #     Enables no extensions by default.
    # :type markdown_extensions: list[str], optional

    # :param rewrite_md_extensions: When True, input files with a ``.md`` extension will have the extension changed to
    #     ``.html`` in the output. Whether you use this or not depends on how you have written your links in the source
    #     code. If you reference your own documents by their ".md" filenames (which is useful in many development
    #     scenarios), you should not enable this or your links will break. Defaults to False.
    # :type rewrite_md_extensions: bool, optional

    :param stylesheet_target_name: Defines an alternate filename to store the stylesheet in the output. By default,
        we use "style.css", but if you already have a file by that name in your sources, it would create a conflict to
        use that name in the output. Use this option to resolve the conflict.
    :type stylesheet_target_name: str, optional

    :raises IOError: When the target directory exists, but you have not provided ``delete_target_dir=True``.
    :raises ValueError: When the stylesheet's target filename conflicts with a filename in the source content.
    """

    # Prepare target directory
    target_path = Path(target_dir)
    if target_path.exists():
        if delete_target_dir:
            log.info(f'Deleting target directory {target_dir}')
            rmtree(target_path)
        else:
            raise IOError(f'Target directory {target_dir} already exists, but you did not specify to delete it.')
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
        rendered_paths.extend(engine.render(source_dir=source_dir, target_dir=target_dir, paths=source_files))
    rendered_paths = set(rendered_paths)

    missed_paths = [path for path in source_files if path not in rendered_paths]

    for path in missed_paths:
        log.debug(f'Copying unrendered file {path}')
        shutil.copy(f'{source_dir}/{path}', f'{target_dir}/{path}')