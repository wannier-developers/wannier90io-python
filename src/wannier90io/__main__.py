import argparse
import re
import pprint

import wannier90io as w90io


pp = pprint.PrettyPrinter(indent=2, width=120)
pprint.sorted = lambda x, key=None: x   # print dictionaries with keys in insertion order


def parse_win(args):
    contents = args.file.read()

    comments = w90io._core.extract_comments(contents)
    parameters = w90io._core.extract_parameters(contents)
    blocks = w90io._core.extract_blocks(contents)

    if args.extract_only:
        pp.pprint({
            'comments': comments,
            'parameters': parameters,
            'blocks': blocks,
        })
    else:
        parsed_win = w90io.parse_win_raw(contents)
        if args.parameters:
            pp.pprint({
                parameter: parsed_win['parameters'][parameter]
                for parameter in args.parameters if parameter in parsed_win['parameters']
            })
        if args.blocks:
            pp.pprint({
                block: parsed_win[block]
                for block in args.blocks if block in parsed_win['blocks']
            })
        if not args.parameters and not args.blocks:
            pp.pprint(parsed_win)


def parse_wout_iteration_info(args):
    parsed_iteration_info = w90io.parse_wout_iteration_info(args.file)

    if args.convergence:
        pp.pprint(parsed_iteration_info['convergence'])

    if args.spread:
        pp.pprint(parsed_iteration_info['spread'])

    if args.delta:
        pp.pprint(parsed_iteration_info['delta'])

    if args.disentanglement:
        pp.pprint(parsed_iteration_info['disentanglement'])

    if not any([args.convergence, args.spread, args.delta, args.disentanglement]):
        pp.pprint(parsed_iteration_info)


def parse_nnkp(args):
    contents = args.file.read()

    comments = w90io._core.extract_comments(contents)
    parameters = w90io._core.extract_parameters(contents)
    blocks = w90io._core.extract_blocks(contents)

    if args.extract_only:
        pp.pprint({
            'comments': comments,
            'parameters': parameters,
            'blocks': blocks,
        })
    else:
        parsed_nnkp = w90io.parse_nnkp_raw(contents)
        if args.parameters:
            pp.pprint({
                parameter: parsed_nnkp['parameters'][parameter]
                for parameter in args.parameters if parameter in parsed_nnkp['parameters']
            })
        if args.blocks:
            pp.pprint({
                block: parsed_nnkp[block]
                for block in args.blocks if block in parsed_nnkp['blocks']
            })
        if not args.parameters and not args.blocks:
            pp.pprint(parsed_nnkp)


def info_amn(args):
    with args.file:
        amn = w90io.read_amn(args.file)

    print(f'Nk = {amn.shape[0]}')
    print(f'Nb = {amn.shape[1]}')
    print(f'Np = {amn.shape[2]}')


def info_eig(args):
    with args.file:
        eig = w90io.read_eig(args.file)

    print(f'Nk = {eig.shape[0]}')
    print(f'Nb = {eig.shape[1]}')


def info_mmn(args):
    with args.file:
        (mmn, nnkpts) = w90io.read_mmn(args.file)

    print(mmn.shape, nnkpts.shape)


def info_chk(args):
    with args.file:
        chk = w90io.read_chk(args.file)

    print(chk['num_bands'])
    print(chk['num_wann'])
    print(chk['have_disentangled'])


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser', required=True)
    #
    parser_common = argparse.ArgumentParser(add_help=False)
    parser_common.add_argument('file', type=open)
    parser_common_parse = argparse.ArgumentParser(add_help=False)
    group = parser_common_parse.add_mutually_exclusive_group()
    group.add_argument('--parameters', type=lambda string: re.split('[ ,]', string))
    group.add_argument('--blocks', type=lambda string: re.split('[ ,]', string))
    #
    parser_win = subparsers.add_parser('parse-win', parents=[parser_common, parser_common_parse])
    parser_win.add_argument('--extract-only', action='store_true')
    parser_win.set_defaults(func=parse_win)
    #
    parser_wout_iteration_info = subparsers.add_parser('parse-wout-iteration-info', parents=[parser_common])
    group = parser_wout_iteration_info.add_mutually_exclusive_group()
    group.add_argument('--convergence', action='store_true')
    group.add_argument('--spread', action='store_true')
    group.add_argument('--delta', action='store_true')
    group.add_argument('--disentanglement', action='store_true')
    parser_wout_iteration_info.set_defaults(func=parse_wout_iteration_info)
    #
    parser_nnkp = subparsers.add_parser('parse-nnkp', parents=[parser_common, parser_common_parse])
    parser_nnkp.add_argument('--extract-only', action='store_true')
    parser_nnkp.set_defaults(func=parse_nnkp)
    #
    parser_info_amn = subparsers.add_parser('info-amn', parents=[parser_common])
    parser_info_amn.set_defaults(func=info_amn)
    #
    parser_info_eig = subparsers.add_parser('info-eig', parents=[parser_common])
    parser_info_eig.set_defaults(func=info_eig)
    #
    parser_info_mmn = subparsers.add_parser('info-mmn', parents=[parser_common])
    parser_info_mmn.set_defaults(func=info_mmn)
    #
    parser_info_chk = subparsers.add_parser('info-chk', parents=[parser_common])
    parser_info_chk.set_defaults(func=info_chk)

    args = parser.parse_args()
    args.func(args)
