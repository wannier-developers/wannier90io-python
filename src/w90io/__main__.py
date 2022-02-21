import argparse
import pprint

import w90io


def parse_win(args):
    with open(args.file, 'r') as fh:
        contents = fh.read()

    comments = w90io._core.extract_comments(contents)
    parameters = w90io._core.extract_parameters(contents)
    blocks = w90io._core.extract_blocks(contents)

    if args.extract_only:
        pprint.pprint({
            'comments': comments,
            'parameters': parameters,
            'blocks': blocks,
        })
    else:
        parsed_win = w90io.parse_win(contents)
        pprint.pprint(parsed_win)


def parse_nnkp(args):
    with open(args.file, 'r') as fh:
        contents = fh.read()

    comments = w90io._core.extract_comments(contents)
    parameters = w90io._core.extract_parameters(contents)
    blocks = w90io._core.extract_blocks(contents)

    if args.extract_only:
        pprint.pprint({
            'comments': comments,
            'parameters': parameters,
            'blocks': blocks,
        })
    else:
        parsed_nnkp = w90io.parse_nnkp(contents)
        pprint.pprint(parsed_nnkp)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', required=True)
    parser_win = subparsers.add_parser('parse-win')
    parser_win.add_argument('file')
    parser_win.add_argument('--extract-only', action='store_true')
    parser_win.set_defaults(func=parse_win)
    parser_nnkp = subparsers.add_parser('parse-nnkp')
    parser_nnkp.add_argument('file')
    parser_nnkp.add_argument('--extract-only', action='store_true')
    parser_nnkp.set_defaults(func=parse_nnkp)

    args = parser.parse_args()
    args.func(args)
