from __future__ import annotations
import re

import numpy as np

from . import _core


__all__ = ['parse_nnkp']


patterns = {
    'lattice_vectors': re.compile(
        rf'(?P<v1>{_core.expressions["3-vector"]})\s+'
        rf'(?P<v2>{_core.expressions["3-vector"]})\s+'
        rf'(?P<v3>{_core.expressions["3-vector"]})',
        re.IGNORECASE | re.DOTALL
    ),
    'kpoints': re.compile(
        r'\d+\s+'
        r'(?P<kpoints>.+)',
        re.IGNORECASE | re.DOTALL
    ),
    'projections': re.compile(
        r'\d+\s+'
        r'(?P<projections>.+)',
        re.IGNORECASE | re.DOTALL
    ),
    'exclude_bands': re.compile(
        r'\d+\s*'
        r'(?P<exclude_bands>.*)',
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


def parse_kpoints(string: str) -> dict:
    match = patterns['kpoints'].search(string)

    return {
        'kpoints': np.fromstring(match.group('kpoints'), sep='\n').reshape((len(match.group('kpoints').splitlines()), -1))[:, :3]
    }


def parse_projections(string: str) -> dict:
    match = patterns['projections'].search(string)

    projections = np.fromstring(match.group('projections'), sep='\n').reshape((-1, 13))

    return [
        {
            'center': projection[:3],
            'l': int(projection[3]),
            'mr': int(projection[4]),
            'r': int(projection[5]),
            'z-axis': projection[6:9],
            'x-axis': projection[9:12],
            'zona': projection[12],
        }
        for projection in projections
    ]


def parse_spinor_projections(string: str) -> dict:
    match = patterns['projections'].search(string)

    projections = np.fromstring(match.group('projections'), sep='\n').reshape((-1, 17))

    return [
        {
            'center': projection[:3],
            'l': int(projection[3]),
            'mr': int(projection[4]),
            'r': int(projection[5]),
            'z-axis': projection[6:9],
            'x-axis': projection[9:12],
            'zona': projection[12],
            'spin': int(projection[13]),
            'spin-axis': projection[14:],
        }
        for projection in projections
    ]


def parse_exclude_bands(string: str) -> dict:
    match = patterns['exclude_bands'].search(string)

    exclude_bands = np.fromstring(match.group('exclude_bands'), sep='\n', dtype=int)

    if exclude_bands.size > 0:
        return {
            'exclude_bands': exclude_bands
        }
    else:
        return {
            'exclude_bands': None
        }


def parse_nnkp(string: str) -> dict:
    """
    Parse NNKP

    Arguments:
        string: the NNKP text

    Returns:
        the parsed NNKP
    """
    comments = _core.extract_comments(string)
    parameters = _core.parse_parameters(_core.extract_parameters(string))
    blocks = _core.parse_blocks(_core.extract_blocks(string))

    parsed_nnkp = {
        'comments': comments,
        'parameters': parameters,
        'blocks': blocks,
        'direct_lattice': parse_direct_lattice(blocks['real_lattice']),
        'reciprocal_lattice': parse_reciprocal_lattice(blocks['recip_lattice']),
        'kpoints': parse_kpoints(blocks['kpoints']),
        'exclude_bands': parse_exclude_bands(blocks['exclude_bands']),
    }
    if 'projections' in 'blocks':
        parsed_nnkp['projections'] = parse_projections(blocks['projections'])
    if 'spinor_projections' in blocks:
        parsed_nnkp['spinor_projections'] = parse_spinor_projections(blocks['spinor_projections'])

    return parsed_nnkp
