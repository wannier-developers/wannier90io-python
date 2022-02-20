from . import _win


def parse_win(string: str) -> dict:
    comments = _win.extract_comments(string)
    parameters = _win.parse_parameters(_win.extract_parameters(string))
    blocks = _win.parse_blocks(_win.extract_blocks(string))

    parsed_win = {
        'comments': comments,
        'parameters': parameters,
        'blocks': blocks,
        'unit_cell': _win.parse_unit_cell(blocks['unit_cell_cart']),
        'kpoints': _win.parse_kpoints(blocks['kpoints']),
    }
    if 'atoms_cart' in blocks:
        parsed_win['atoms_cart'] = _win.parse_atoms(blocks['atoms_cart'])
    if 'atoms_frac' in blocks:
        parsed_win['atoms_frac'] = _win.parse_atoms(blocks['atoms_frac'])
    if 'projections' in blocks:
        parsed_win['projections'] = _win.parse_projections(blocks['projections'])

    return parsed_win
