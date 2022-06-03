import pathlib

import pytest

import w90io


@pytest.mark.parametrize('example', [f'example{i:02d}' for i in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20]])
def test_parse_nnkp(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.nnkp', 'r') as fh:
        contents = fh.read()

    try:
        w90io.parse_nnkp_raw(contents)
    except Exception:
        assert False
