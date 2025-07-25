"""
Main entrypoint to the microsite command line utility.
"""

import logging
import tomllib

from argparse import ArgumentParser
from copy import deepcopy
from microsite.publish.s3 import TbPulumiS3Website
from microsite.render.markdown import MarkdownRenderEngine
from microsite.util import AttrDict


DEFAULT_PROJECT_CONFIG = {
    'render': {
        'source': None,
        'target': 'output/',
        'delete_target_dir': True,
        'engines': ['markdown'],
        'engine': {
            'markdown': {
                'extensions': ['tables', 'md_in_html'],
                'html_template': 'markdown.html.j2',
                'pretty_html': False,
                'rewrite_md_extensions': True,
                'rewrite_md_urls': True,
                'stylesheet': 'microsite/render/styles/plain-white.css',
                'stylesheet_target_name': 'style.css',
                'title': '',
            }
        },
    }
}

MARKDOWN_EXTENSION_DOCS_URL = 'https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/index.md#officially-supported-extensions'

PUBLISH_ENGINE_CLASS_MAP = {
    'tbp_s3website': TbPulumiS3Website,
}

RENDER_ENGINE_CLASS_MAP = {
    'markdown': MarkdownRenderEngine,
}


def parse_args() -> None:
    """
    Parse the command line arguments this program has been initiated with.
    """

    # Base parser
    parser = ArgumentParser(
        prog='microsite', description='Tools for publishing Markdown content as static websites.'
    )
    parser.add_argument(
        'project',
        help='TOML file containing the settings for your project',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='Produce additional output for debugging purposes',
        default=False,
        action='store_true',
    )
    subparsers = parser.add_subparsers(help='Runmode for the tool', dest='runmode')
    _render_parser = subparsers.add_parser(
        'render', help='Run in render mode to convert content into web content'
    )
    publish_parser = subparsers.add_parser(
        'publish',
        help='Run in publish mode to alter a live site',
    )
    publish_parser.add_argument(
        '-d',
        '--dry-run',
        help=(
            'Do not perform any actions that affect a live site, but log the actions that would '
            'have been taken otherwise.'
        ),
        default=False,
        action='store_true',
    )
    publish_parser.add_argument(
        '-x',
        '--destroy',
        help='Destroy this site and its infrastructure.',
        default=False,
        action='store_true',
    )

    return parser.parse_args()


def get_config(config_file: str) -> AttrDict:
    config = deepcopy(DEFAULT_PROJECT_CONFIG)
    with open(config_file, 'rb') as fh:
        config.update(tomllib.load(fh))

    return AttrDict(config)


def setup_logging(verbose: bool = False) -> None:
    """
    Configure the logging facility this program will use.

    :param verbose: When True, extra detail is produced in the logs. Defaults to False.
    :type verbose: bool, optional
    """

    log = logging.getLogger(__name__)

    log_format = (
        '[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s' if verbose else '%(message)s'
    )
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=log_format,
    )
    log.info('Logging configured.')
    log.debug('Log verbosity enabled.')


def main() -> None:
    """
    Main CLI tool entrypoint.
    """

    # Get configured, announce readiness!
    args = parse_args()
    setup_logging(verbose=args.verbose)
    logging.debug(f'Program started with args: {args}')
    logging.debug(f'Running in {args.runmode} mode')

    # Load the project config file
    project = get_config(args.project)

    # Render Mode
    if args.runmode == 'render':
        from microsite.render import render

        render_engines = [
            RENDER_ENGINE_CLASS_MAP[engine](config=AttrDict(project.render.engine[engine]))
            for engine in project.render.engines
        ]

        render(
            engines=render_engines,
            source_dir=project.render.source,
            target_dir=project.render.target,
            delete_target_dir=project.render.delete_target_dir,
        )

    # Publish Mode
    if args.runmode == 'publish':
        for target in project.publish.targets:
            target_config = AttrDict(project.publish.targets[target])
            PUBLISH_ENGINE_CLASS_MAP[target_config.engine](
                name=target,
                source_dir=project.publish.source,
                config=target_config,
                dry_run=args.dry_run,
                destroy=args.destroy,
            ).publish()


if __name__ == '__main__':
    main()
