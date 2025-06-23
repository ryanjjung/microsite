"""
Main entrypoint to the microsite command line utility.
"""

import logging

from argparse import ArgumentParser


MARKDOWN_EXTENSION_DOCS_URL = (
    'https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/index.md#officially-supported-extensions'
)


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
        '-r',
        '--rewrite-md-extensions',
        help='Rewrite source files with .md extensions as .html files in the output',
        default=False,
        action='store_true',
    )
    sub_render.add_argument(
        '-s',
        '--stylesheet',
        help='Path to stylesheet to package with your site.',
        default='microsite/render/styles/plain-white.css',
    )
    sub_render.add_argument(
        '--stylesheet-target-name',
        help=(
            'The filename to install the stylesheet to. Use when there is a filename conflict between your source and'
            'the destination for the stylesheet in your rendered output.'
        ),
        default=None,
    )
    sub_render.add_argument(
        '-t',
        '--template',
        help='Path to the Jinja2 template to render Markdown files into.',
        default='microsite/render/templates/default.html.j2',
    )
    sub_render.add_argument(
        '-x',
        '--extension',
        help=f'Enable a Markdown extension; see {MARKDOWN_EXTENSION_DOCS_URL}',
        action='append',
        dest='extensions',
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
        from microsite.render import render_dir

        render_dir(
            source_dir=args.source,
            target_dir=args.target,
            stylesheet=args.stylesheet,
            template=args.template,
            delete_target_dir=args.delete_target_dir,
            markdown_extensions=args.extensions if args.extensions else [],
            rewrite_md_extensions=args.rewrite_md_extensions,
            stylesheet_target_name=args.stylesheet_target_name,
        )
    if args.runmode == 'publish':
        logging.info('Not yet implemented!')


if __name__ == '__main__':
    main()
