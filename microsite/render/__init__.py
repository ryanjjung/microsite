"""
This program accepts a source directory containing static assets (such as images, fonts, etc.) and Markdown text files.
It produces a target directory containing that content rendered as a static webpage which can be uploaded to any file
host.
"""

import jinja2
import logging
import shutil

from markdown import markdown
from microsite import path as ms_path
from shutil import rmtree
from pathlib import Path


log = logging.getLogger(__name__)


def render_dir(
    source_dir: str,
    target_dir: str,
    stylesheet: str,
    template: str,
    delete_target_dir: bool = False,
    markdown_extensions: list[str] = [],
    stylesheet_target_name: str = None,
):
    """
    Discover all files contained within ``source_dir``. Render any Markdown files into HTML files stored in the
    ``target_dir``. Copy any other files directly over.

    :param source_dir: Path to the top level directory containing the content to render.
    :type source_dir: str

    :param target_dir: Path to the top level directory to render output into.
    :type target_dir: Path
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

    # Copy in the stylesheet; detect potential filename conflicts
    if not stylesheet_target_name:
        stylesheet_target_name = 'style.css'
    if stylesheet_target_name in source_files:
        raise ValueError(
            f"The stylesheet's filename ({stylesheet_target_name}) conflicts with a filename in the source content. "
            'Specify an alternate stylesheet target name.'
        )
    shutil.copy(stylesheet, f'{target_dir}/{stylesheet_target_name}')

    # Do something with each source file
    for file in source_files:
        log.debug(f'Inspecting {source_dir}{file}')
        if Path(f'{source_dir}{file}').is_file():
            # Ensure the target containing directory exists
            target_subdir = Path('/'.join(f'{target_dir}/{file}'.split('/')[:-1]))
            target_subdir.mkdir(exist_ok=True, parents=True)

            if file.endswith('.md'):
                # Replace .md extension with .html
                file_parts = file.split('.')
                file_parts[-1] = 'html'
                target_filename = '.'.join(file_parts)
                render_markdown_file(
                    source_dir=source_dir,
                    source_file=file,
                    target_file=f'{target_dir}/{target_filename}',
                    stylesheet=stylesheet_target_name,
                    markdown_extensions=markdown_extensions,
                )
            else:
                # Copy the file directly
                shutil.copy(f'{source_dir}/{file}', f'{target_dir}/{file}')


def render_markdown_file(
    source_dir: str,
    source_file: str,
    target_file: str,
    stylesheet: str,
    markdown_extensions: list[str] = [],
):
    # Path-ify some things
    source = Path(f'{source_dir}/{source_file}')
    target = Path(target_file)
    template = 'default.html.j2'

    # Convert the Markdown to HTML (but this is only a snippet, not a full proper document)
    md_html = ''
    if not source.is_file():
        raise ValueError(f'Source file {source_file} is not a normal file.')
    with source.open('r') as file:
        log.debug(f'Rendering Markdown from source {source} into HTML')
        md_html = markdown(file.read(), extensions=markdown_extensions)

    # Pipe that HTML into a Jinja template with other rendering details
    log.info(f'Rendering {source_dir}{source_file} to {target_file}')
    log.debug(f'Rendering template for source {source}')
    j2_loader = jinja2.FileSystemLoader(searchpath='microsite/render/templates/')
    j2_env = jinja2.Environment(loader=j2_loader)
    j2_tpl = j2_env.get_template(template)
    dots = '../' * (len(source_file.split('/')) - 1)
    relative_stylesheet = f'{dots}{stylesheet}'
    page_html = j2_tpl.render(stylesheet=relative_stylesheet, title='TODO!', html=md_html)

    # Write out the content to the target
    with target.open('w') as file:
        log.debug(f'Writing target file {target}')
        file.write(page_html)
