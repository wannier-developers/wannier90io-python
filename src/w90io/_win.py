from __future__ import annotations
import re

from . import _core

import numpy as np


__all__ = ['parse_win']


patterns = {
    'unit_cell': re.compile(
        r'((?P<units>bohr|ang)\s+)?'
        rf'(?P<a1>{_core.expressions["3-vector"]})\s+'
        rf'(?P<a2>{_core.expressions["3-vector"]})\s+'
        rf'(?P<a3>{_core.expressions["3-vector"]})',
        re.IGNORECASE | re.DOTALL
    ),
    'atoms': re.compile(
        r'((?P<units>bohr|ang)\s+)?'
        rf'(?P<atoms>([ \t]*\w+[ \t]+{_core.expressions["3-vector"]}\s*)+)',
        re.IGNORECASE | re.DOTALL
    ),
    'projections': re.compile(
        r'((?P<units>bohr|ang)\s+)?'
        r'(?P<projections>.+)',
        re.IGNORECASE | re.DOTALL
    ),
}


def parse_unit_cell(string: str) -> dict:
    match = patterns['unit_cell'].search(string)

    if match is not None:
        a1 = np.fromstring(match.group('a1'), sep=' ')
        a2 = np.fromstring(match.group('a2'), sep=' ')
        a3 = np.fromstring(match.group('a3'), sep=' ')

        return {
            'units': match.group('units'),
            'a1': a1, 'a2': a2, 'a3': a3,
            'lattice_vectors': np.array([a1, a2, a3]),
        }
    else:
        return None


def parse_atoms(string: str) -> dict:
    match = patterns['atoms'].search(string)

    if match is not None:
        return {
            'units': match.group('units'),
            'atoms': [
                {
                    'species': line.split()[0],
                    'basis_vector': np.fromiter(map(float, line.split()[1:]), dtype=float),
                }
                for line in match.group('atoms').splitlines()
            ]
        }
    else:
        return None


def parse_projections(string: str) -> dict:
    match = patterns['projections'].search(string)

    if match is not None:
        return {
            'units': match.group('units'),
            'projections': match.group('projections').splitlines(),
        }
    else:
        return None


def parse_kpoints(string: str) -> dict:
    return {
        'kpoints': np.fromstring(string, sep='\n').reshape((len(string.splitlines()), -1))[:, :3]
    }


def parse_win(string: str) -> dict:
    """
    Parse WIN

    Arguments:
        string: the WIN text

    Returns:
        the parsed WIN
    """
    comments = _core.extract_comments(string)
    parameters = _core.parse_parameters(_core.extract_parameters(string))
    blocks = _core.parse_blocks(_core.extract_blocks(string))

    parsed_win = {
        'comments': comments,
        'parameters': parameters,
        'blocks': blocks,
    }
    if 'unit_cell_cart' in blocks:
        parsed_win['unit_cell_cart'] = parse_unit_cell(blocks['unit_cell_cart'])
    if 'atoms_cart' in blocks:
        parsed_win['atoms_cart'] = parse_atoms(blocks['atoms_cart'])
    if 'atoms_frac' in blocks:
        parsed_win['atoms_frac'] = parse_atoms(blocks['atoms_frac'])
    if 'projections' in blocks:
        parsed_win['projections'] = parse_projections(blocks['projections'])
    if 'kpoints' in blocks:
        parsed_win['kpoints'] = parse_kpoints(blocks['kpoints'])

    return parsed_win
