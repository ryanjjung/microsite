"""
This program accepts a source directory containing static assets (such as images, fonts, etc.) and Markdown text files.
It produces a target directory containing that content rendered as a static webpage which can be uploaded to any file
host.
"""

import logging

from microsite import path as ms_path
from pathlib import Path


log = logging.getLogger(__name__)

def render(source_dir: str, target_dir: Path):
    """
    Discover all files contained within ``source_dir``. Render any Markdown files into HTML files stored in the
    ``target_dir``. Copy any other files directly over.

    :param source_dir: Path to the top level directory containing the content to render.
    :type source_dir: str

    :param target_dir: Path to the top level directory to render output into.
    :type target_dir: Path
    """
    
    log.debug(f'Rendering the contents of {source_dir} into {target_dir}')
    ms_path.validate_dir(source_dir)
    source_files = ms_path.get_all_paths(source_dir=source_dir)
    log.debug('Found the following files:')
    for file in source_files:
        log.debug(str(file))
    
    # Detect Markdown files by file extension
    markdown_files = [ file for file in source_files if str(file).endswith('.md') ]
    log.debug('Found the following Markdown files:')
    for file in markdown_files:
        log.debug(str(file))