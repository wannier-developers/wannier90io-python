from __future__ import annotations
import re

from . import _core

import numpy as np


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
