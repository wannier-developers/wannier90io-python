import pathlib

import pytest

import wannier90io as w90io


@pytest.mark.parametrize('example', [f'example{i:02d}' for i in [1, 2, 3, 4]])
def test_parse_wout(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.wout', 'r') as fh:
        try:
            w90io.parse_wout_iteration_info(fh)
        except Exception:
            assert False
