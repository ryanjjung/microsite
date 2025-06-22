"""
This program accepts (among other things) a directory containing static assets (such as images, fonts, etc.) and
Markdown text files. It produces a directory containing that content rendered as a static webpage which can be uploaded
to any file host.
"""

import logging

from argparse import ArgumentParser


def parse_args():
    """
    Parse the command line arguments this program has been initiated with.
    """

    parser = ArgumentParser(
        prog='python -m markdown-publisher', description='Renders a directory containing Markdown files into an HTML website.'
    )
    parser.add_argument('source', help='Directory where the source content can be found.')
    parser.add_argument('target', help='Directory where the output should be created.')
    parser.add_argument(
        '-v', '--verbose', help='Produce additional output for debugging purposes', default=False, action='store_true'
    )
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


if __name__ == '__main__':
    main()
