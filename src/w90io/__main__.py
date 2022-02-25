import argparse
import re
import pprint

import w90io


def parse_win(args):
    contents = args.file.read()

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
        if args.parameters:
            pprint.pprint({
                parameter: parsed_win['parameters'][parameter]
                for parameter in args.parameters if parameter in parsed_win['parameters']
            })
        if args.blocks:
            pprint.pprint({
                block: parsed_win[block]
                for block in args.blocks if block in parsed_win['blocks']
            })
        if not args.parameters and not args.blocks:
            pprint.pprint(parsed_win)


def parse_nnkp(args):
    contents = args.file.read()

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
        if args.parameters:
            pprint.pprint({
                parameter: parsed_nnkp['parameters'][parameter]
                for parameter in args.parameters if parameter in parsed_nnkp['parameters']
            })
        if args.blocks:
            pprint.pprint({
                block: parsed_nnkp[block]
                for block in args.blocks if block in parsed_nnkp['blocks']
            })
        if not args.parameters and not args.blocks:
            pprint.pprint(parsed_nnkp)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', required=True)
    #
    parser_common = argparse.ArgumentParser(add_help=False)
    parser_common.add_argument('file', type=open)
    parser_common.add_argument('--extract-only', action='store_true')
    group = parser_common.add_mutually_exclusive_group()
    group.add_argument('--parameters', type=lambda string: re.split('[ ,]', string))
    group.add_argument('--blocks', type=lambda string: re.split('[ ,]', string))
    #
    parser_win = subparsers.add_parser('parse-win', parents=[parser_common])
    parser_win.set_defaults(func=parse_win)
    #
    parser_nnkp = subparsers.add_parser('parse-nnkp', parents=[parser_common])
    parser_nnkp.set_defaults(func=parse_nnkp)

    args = parser.parse_args()
    args.func(args)
