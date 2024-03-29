import pathlib

import pytest

import wannier90io as w90io


@pytest.mark.parametrize('example', [f'example{i:02d}' for i in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20]])
def test_parse_nnkp(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.nnkp', 'r') as fh:
        contents = fh.read()

    try:
        parsed_nnkp = w90io.parse_nnkp_raw(contents)
    except Exception:
        assert False

    try:
        w90io._schema.NNKP.parse_obj(parsed_nnkp)
    except Exception:
        assert False
