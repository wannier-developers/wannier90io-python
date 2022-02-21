from __future__ import annotations
import re

import numpy as np

from . import _core


patterns = {
    'lattice_vectors': re.compile(
        rf'(?P<v1>{_core.expressions["3-vector"]})\s+'
        rf'(?P<v2>{_core.expressions["3-vector"]})\s+'
        rf'(?P<v3>{_core.expressions["3-vector"]})',
        re.IGNORECASE | re.DOTALL
    ),
}


def parse_lattice(string: str) -> dict:
    match = patterns['lattice_vectors'].search(string)

    if match is not None:
        v1 = np.fromstring(match.group('v1'), sep=' ')
        v2 = np.fromstring(match.group('v2'), sep=' ')
        v3 = np.fromstring(match.group('v3'), sep=' ')

        return {
            'v1': v1, 'v2': v2, 'v3': v3,
            'lattice_vectors': np.array([v1, v2, v3]),
        }
    else:
        return None


def parse_direct_lattice(string: str) -> dict:
    lattice = parse_lattice(string)

    return {
        'a1': lattice['v1'], 'a2': lattice['v2'], 'a3': lattice['v3'],
        'lattice_vectors': lattice['lattice_vectors']
    }


def parse_reciprocal_lattice(string: str) -> dict:
    lattice = parse_lattice(string)

    return {
        'b1': lattice['v1'], 'b2': lattice['v2'], 'b3': lattice['v3'],
        'lattice_vectors': lattice['lattice_vectors']
    }
