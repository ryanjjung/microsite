"""
Main entrypoint to the microsite command line utility. Also contains code common to all modules.
"""

import logging

from argparse import ArgumentParser
# from pathlib import Path


def parse_args():
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

    return parser.parse_args()


def setup_logging(verbose: bool = False):
    """
    Configure the logging facility this program will use.
    """

    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format='[%(asctime)s] %(module)s %(message)s')
    log.info('Logging configured.')
    log.debug('Log verbosity enabled.')


def main():
    args = parse_args()
    setup_logging(verbose=args.verbose)
    logging.debug(f'Program started with args: {args}')


if __name__ == '__main__':
    main()
