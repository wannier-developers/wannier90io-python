from __future__ import annotations

from . import _core
from . import _nnkp
from . import _win


def parse_win(string: str) -> dict:
    comments = _core.extract_comments(string)
    parameters = _core.parse_parameters(_core.extract_parameters(string))
    blocks = _core.parse_blocks(_core.extract_blocks(string))

    parsed_win = {
        'comments': comments,
        'parameters': parameters,
        'blocks': blocks,
    }
    if 'unit_cell_cart' in blocks:
        parsed_win['unit_cell'] =_win.parse_unit_cell(blocks['unit_cell_cart'])
    if 'atoms_cart' in blocks:
        parsed_win['atoms_cart'] = _win.parse_atoms(blocks['atoms_cart'])
    if 'atoms_frac' in blocks:
        parsed_win['atoms_frac'] = _win.parse_atoms(blocks['atoms_frac'])
    if 'projections' in blocks:
        parsed_win['projections'] = _win.parse_projections(blocks['projections'])
    if 'kpoints' in blocks:
        parsed_win['kpoints'] =_win.parse_kpoints(blocks['kpoints'])

    return parsed_win


def parse_nnkp(string: str) -> dict:
    comments = _core.extract_comments(string)
    parameters = _core.parse_parameters(_core.extract_parameters(string))
    blocks = _core.parse_blocks(_core.extract_blocks(string))

    parsed_nnkp = {
        'comments': comments,
        'parameters': parameters,
        'blocks': blocks,
        'direct_lattice': _nnkp.parse_direct_lattice(blocks['real_lattice']),
        'reciprocal_lattice': _nnkp.parse_reciprocal_lattice(blocks['recip_lattice']),
        'kpoints': _nnkp.parse_kpoints(blocks['kpoints']),
        'exclude_bands': _nnkp.parse_exclude_bands(blocks['exclude_bands']),
    }
    if 'projections' in 'blocks':
        parsed_nnkp['projections'] = _nnkp.parse_projections(blocks['projections'])
    if 'spinor_projections' in blocks:
        parsed_nnkp['spinor_projections'] = _nnkp.parse_spinor_projections(blocks['spinor_projections'])

    return parsed_nnkp
