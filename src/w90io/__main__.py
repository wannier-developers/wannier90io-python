import argparse
import pprint

import w90io


def parse_win(args):
    with open(args.file, 'r') as fh:
        contents = fh.read()

    comments = w90io._win.extract_comments(contents)
    parameters = w90io._win.extract_parameters(contents)
    blocks = w90io._win.extract_blocks(contents)

    if args.extract_only:
        pprint.pprint({
            'comments': comments,
            'parameters': parameters,
            'blocks': blocks,
        })
    else:
        parsed_win = w90io.parse_win(contents)
        pprint.pprint(parsed_win)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', required=True)
    parser_win = subparsers.add_parser('parse-win')
    parser_win.add_argument('file')
    parser_win.add_argument('--extract-only', action='store_true')
    parser_win.set_defaults(func=parse_win)

    args = parser.parse_args()
    args.func(args)
