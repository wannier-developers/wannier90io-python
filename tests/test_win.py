import pathlib

import pytest

import w90io._win


@pytest.mark.parametrize('example', [f'example{i:02d}' for i in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20]])
def test_parse_win(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.win', 'r') as fh:
        contents = fh.read()

    try:
        w90io.parse_win(contents)
    except Exception:
        assert False
