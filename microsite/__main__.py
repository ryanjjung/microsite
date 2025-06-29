"""
Main entrypoint to the microsite command line utility.
"""

import logging

from argparse import ArgumentParser
from microsite.render.eng_markdown import MarkdownRenderEngine


MARKDOWN_EXTENSION_DOCS_URL = (
    'https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/index.md#officially-supported-extensions'
)

RENDER_ENGINE_CLASS_MAP = {
    'markdown': MarkdownRenderEngine,
}


def parse_args() -> None:
    """
    Parse the command line arguments this program has been initiated with.
    """

    # Base parser
    parser = ArgumentParser(prog='microsite', description='Tools for publishing Markdown content as static websites.')
    parser.add_argument(
        '-v', '--verbose', help='Produce additional output for debugging purposes', default=False, action='store_true'
    )

    # Add subparsers for each subcommand
    subparsers = parser.add_subparsers(dest='runmode')

    # Subparser for publishing step
    sub_publish = subparsers.add_parser('publish', help='Publish static content to an online target.')
    sub_publish.add_argument('source', help='Directory containing the pre-rendered content to publish.')
    sub_publish.add_argument('target', help='URI describing the publication target.')

    # Subparser for the rendering step
    sub_render = subparsers.add_parser('render', help='Render Markdown documents into HTML files.')
    sub_render.add_argument('source', help='Directory where the source content can be found.')
    sub_render.add_argument('target', help='Directory where the output should be created.')
    sub_render.add_argument(
        '-d',
        '--delete-target-dir',
        help='Delete the target directory before rendering the source.',
        default=False,
        action='store_true',
    )
    sub_render.add_argument(
        '-e',
        '--engine',
        help='Enable the use of a supported rendering engine.',
        default=[],
        action='append',
        dest='engines',
        choices=['markdown'],
    )

    # Markdown Rendering Engine Options
    sub_render.add_argument(
        '--eng-markdown-rewrite-md-extensions',
        help='Rewrite source files with .md extensions as .html files in the output. Requires `--engine=markdown`.',
        action='store_true',
        default=False,
    )
    sub_render.add_argument(
        '--eng-markdown-html-template',
        help='Path to a Jinja2 template that inserts an HTML snippet into a full HTML document.',
        default='microsite/render/templates/markdown.html.j2',
    )
    sub_render.add_argument(
        '--eng-markdown-template-dir',
        help='Path to the directory containing templates for the Markdown engine.',
        default='microsite/render/templates',
    )
    sub_render.add_argument(
        '--eng-markdown-extension',
        help=f'Enable a Markdown extension; see {MARKDOWN_EXTENSION_DOCS_URL}',
        action='append',
        dest='eng_markdown_extensions',
        default=[],
    )
    sub_render.add_argument(
        '--eng-markdown-stylesheet',
        help='Path to stylesheet to package with your site.',
        default='microsite/render/styles/plain-white.css',
    )
    sub_render.add_argument(
        '--eng-markdown-stylesheet-target-name',
        help=(
            'The filename to install the stylesheet to. Use when there is a filename conflict between your source and'
            'the destination for the stylesheet in your rendered output.'
        ),
        default='style.css',
    )

    return parser.parse_args()


def setup_logging(verbose: bool = False) -> None:
    """
    Configure the logging facility this program will use.

    :param verbose: When True, extra detail is produced in the logs. Defaults to False.
    :type verbose: bool, optional
    """

    log = logging.getLogger(__name__)

    log_format = '[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s' if verbose else '%(message)s'
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=log_format,
    )
    log.info('Logging configured.')
    log.debug('Log verbosity enabled.')


def main() -> None:
    """
    Main entrypoint.
    """

    args = parse_args()
    setup_logging(verbose=args.verbose)
    logging.debug(f'Program started with args: {args}')
    logging.debug(f'Running in {args.runmode} mode')

    if args.runmode == 'render':
        from microsite.render import render

        render_engines = [
            RENDER_ENGINE_CLASS_MAP[engine](
                config={key: value for key, value in vars(args).items() if key.startswith(f'eng_{engine}_')}
            )
            for engine in args.engines
        ]

        render(
            engines=render_engines,
            source_dir=args.source,
            target_dir=args.target,
            delete_target_dir=args.delete_target_dir,
        )
    if args.runmode == 'publish':
        logging.info('Not yet implemented!')


if __name__ == '__main__':
    main()
