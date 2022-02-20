import argparse
import pprint

import w90io._win


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
        parameters = w90io._win.parse_parameters(parameters)
        blocks = w90io._win.parse_blocks(blocks)

        parsed_win = {
            'comments': comments,
            'parameters': parameters,
            'blocks': blocks,
            'unit_cell': w90io._win.parse_unit_cell(blocks['unit_cell_cart']),
            'kpoints': w90io._win.parse_kpoints(blocks['kpoints']),
        }
        if 'atoms_cart' in blocks:
            parsed_win['atoms_cart'] = w90io._win.parse_atoms(blocks['atoms_cart'])
        if 'atoms_frac' in blocks:
            parsed_win['atoms_frac'] = w90io._win.parse_atoms(blocks['atoms_frac'])
        if 'projections' in blocks:
            parsed_win['projections'] = w90io._win.parse_projections(blocks['projections'])

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
