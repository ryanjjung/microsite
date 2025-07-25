import jinja2
import logging
import shutil

from bs4 import BeautifulSoup
from markdown import markdown
from microsite.render import RenderEngine
from microsite.util import AttrDict
from pathlib import Path

log = logging.getLogger(__name__)


class MarkdownRenderEngine(RenderEngine):
    def __init__(self, config: AttrDict, index: dict = {}):
        super().__init__(name='markdown', config=config, index=index)

        # Convert template path string to proper Path
        self.html_template = Path(
            self.config.html_template or 'microsite/render/templates/markdown.html.j2'
        )

        # Resolve any pathing complications like symlinks into "real" paths
        self.html_template = Path.resolve(self.html_template)

    def render(self, source_dir: str, target_dir: str, paths: list[str]) -> list[str]:
        """
        Searches the ``paths`` to find Markdown files by filenames ending in ``.md``. Renders the
        Jinja2 template found at the configured path (``template_dir/html_template``) for each such
        file, inserting HTML rendered from the source Markdown into the output. Copies the
        configured ``stylesheet`` into the source directory using the ``stylesheet_target_name`` and
        inserts a reference to it into each rendered HTML document. The Markdown rendering engine is
        initialized using the configured list of ``extensions``. A full list of available engines
        can be found here:
        https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/index.md#officially-supported-extensions

        :param source_dir: Top-level directory containing source files to render.
        :type source_dir: str | Path

        :param target_dir: Top-level directory to render files into.
        :type target_dir: str | Path

        :param paths: List of all paths in the source directory to be processed. Not every path in
            this list will be rendered.
        :type paths: list[str]

        :return: List of paths this RenderEngine made alterations to.
        :rtype: list[str]
        """

        # Copy in the stylesheet; detect potential filename conflicts
        if self.config.stylesheet_target_name in paths:
            raise ValueError(
                f"The stylesheet's filename ({self.config.stylesheet_target_name}) "
                'conflicts with a filename in the source content. '
                'Specify an alternate stylesheet target name.'
            )
        shutil.copy(
            self.config.stylesheet or 'microsite/render/styles/plain-white.css',
            f'{target_dir}/{self.config.stylesheet_target_name}',
        )

        rendered_paths = []
        for path in paths:
            log.debug(f'Inspecting {source_dir}{path}')
            if Path(f'{source_dir}{path}').is_file():
                # Ensure the deeper target directory exists
                target_subdir = Path('/'.join(f'{target_dir}/{path}'.split('/')[:-1]))
                target_subdir.mkdir(exist_ok=True, parents=True)

                # Render presumed Markdown files
                if path.endswith('.md'):
                    if self.config.rewrite_md_extensions:
                        # Replace .md extension with .html
                        file_parts = path.split('.')
                        file_parts[-1] = 'html'
                        target_filename = '.'.join(file_parts)
                    else:
                        target_filename = path
                    rendered_paths.append(path)
                    self.render_markdown_file(
                        source_dir=source_dir,
                        source_file=path,
                        target_file=f'{target_dir}{target_filename}',
                    )
        return rendered_paths

    def render_markdown_file(
        self,
        source_dir: str,
        source_file: str,
        target_file: str,
    ) -> None:
        """
        Renders a single Markdown file as an HTML file.

        :param source_dir: Directory in which the source file can be found. Used for determining
            relative paths.
        :type source_dir: str

        :param source_file: File to render, relative to the source_dir.
        :type source_file: str

        :param target_file: File to output the rendered HTML into.
        :type target_file: str

        :param stylesheet: Stylesheet file to use.
        :type stylesheet: str

        :param markdown_extensions: List of Markdown extensions to enable. See
            https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/index.md#officially-supported-extensions
            Enables no extensions by default.
        :type markdown_extensions: list[str], optional

        :raises ValueError: When the provided source file is something other than an ordinary file.
        """

        # Path-ify some things
        source = Path(f'{source_dir}/{source_file}')
        target = Path(target_file)

        # Determine the containing directory from the template path; remove path portion of template
        _html_template = str(self.html_template)
        _template_dir = '/'.join(_html_template.split('/')[:-1])
        _html_template = _html_template.split('/')[-1]

        # Convert the Markdown to HTML (but this is only a snippet, not a full proper document)
        md_html = ''
        if not source.is_file():
            raise ValueError(f'Source file {source_file} is not a normal file.')
        with source.open('r') as file:
            log.debug(f'Rendering Markdown from source {source} into HTML')
            md_html = markdown(file.read(), extensions=self.config.extensions)

        # Pipe that HTML into a Jinja template with other rendering details
        log.info(f'Rendering {source_dir}{source_file} to {target_file}')
        log.debug(f'Rendering template for source {source}')
        j2_loader = jinja2.FileSystemLoader(searchpath=_template_dir)
        j2_env = jinja2.Environment(loader=j2_loader)
        j2_tpl = j2_env.get_template(_html_template)
        dots = '../' * (len(source_file.split('/')) - 1)
        relative_stylesheet = f'{dots}{self.config.stylesheet_target_name}'

        # Get the index config
        index = AttrDict(self.index.get(source_file, {}))
        title = index.title if index.title else self.config.title

        page_html = j2_tpl.render(stylesheet=relative_stylesheet, title=title, html=md_html)

        # Convert to a BS object so we can manipulate it before writing it back out
        page_html = BeautifulSoup(page_html, features='html.parser')

        if self.config.rewrite_md_urls:
            page_html = self.rewrite_md_urls(page_html)

        if self.config.pretty_html:
            page_html = str(page_html.prettify())
        else:
            page_html = str(page_html).replace('\n', '')

        # Write out the content to the target
        with target.open('w') as file:
            log.debug(f'Writing target file {target}')
            file.write(page_html)

    def rewrite_md_urls(self, html: BeautifulSoup) -> str:
        log.info('Rewriting URLs in links...')
        for a_tag in html.find_all('a'):
            old_href = href = a_tag.get('href')
            if href and href.endswith('.md') and not href.startswith('http'):
                href = href.split('.')
                href[-1] = 'html'
                href = '.'.join(href)
                a_tag['href'] = href
                log.debug(f'Rewriting {old_href} as {href}')
        return html
