# -*- coding: utf-8 -*-
# ahds.py
"""

Main entry point for console.

"""

from __future__ import print_function

import argparse
import os
import sys

# to use relative syntax make sure you have the package installed in a virtualenv in develop mode e.g. use
# pip install -e /path/to/folder/with/setup.py
# or
# python setup.py develop
from . import AmiraFile, WIDTH
from .core import _str


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(prog='ahds', description='Python tool to read and display Amira files')
    parser.add_argument('file', nargs='+', help='a valid Amira file with an optional block path')
    parser.add_argument('-s', '--load-streams', default=False, action='store_true',
                        help="whether to load data streams or not [default: False]")
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help="display debugging information [default: False]")
    parser.add_argument('-l', '--literal', default=False, action='store_true',
                        help="display the literal header [default: False]")

    args = parser.parse_args()
    return args


def main(): # pragma: nocover
    # TODO come up with appropriate test if required for coverage
    args = parse_args()

    _file, _paths = set_file_and_paths(args)

    af = get_amira_file(_file, args)

    print(get_literal(af, args))

    print(get_debug(af, args))

    print(get_paths(_paths, af))
    return os.EX_OK


def get_amira_file(_file, args):
    af = AmiraFile(_file, load_streams=args.load_streams, debug=args.debug)
    return af


def get_paths(_paths, af):
    if _paths:
        string = ""
        for _path in _paths:
            _path_list = _path.split('.')
            current_block = af  # the AmiraFile object
            for block in _path_list:
                current_block = getattr(current_block, block, None)
            if current_block is None:
                print("""Path '{}' not found.""".format(_path)) # pragma: nocover
            else:
                string += u'*' * WIDTH + u'\n'
                string += u"ahds: Displaying path '{}'\n".format(_path)
                string += u"-" * WIDTH + "\n"
                string += _str(current_block)
    else:
        string = _str(af)
    return string


def get_debug(af, args):
    string = ""
    if args.debug:
        from pprint import pformat
        string += u"*" * WIDTH + "\n"
        string += u"ahds: Displaying parsed header data\n"
        string += u"-" * WIDTH + "\n"
        string += pformat(af.parsed_data) + '\n'
    return string


def get_literal(af, args):
    string = u""
    if args.literal:
        string += u'*' * WIDTH + u'\n'
        string += u"ahds: Displaying literal header\n"
        string += u"-" * WIDTH + "\n"
        string += _str(af.header.literal_data)
    return string


def set_file_and_paths(args):
    if len(args.file) == 1:
        _file = args.file[0]
        _paths = None
    else:
        _file = args.file[0]
        _paths = args.file[1:]
    return _file, _paths


if __name__ == "__main__":
    sys.exit(main()) # pragma: nocover