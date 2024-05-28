import pathlib

import numpy as np
import pytest

import wannier90io as w90io


@pytest.mark.parametrize('example', ['example01'])
def test_read_unk_formatted(wannier90, example):
    for ikpt in range(1, 8+1):
        with open(pathlib.Path(wannier90)/f'examples/{example}/UNK0000{ikpt}.1', 'r') as fh:
            (ikpt_parsed, wvfn) = w90io.read_unk_formatted(fh)
        assert ikpt == ikpt_parsed

        ngx, ngy, ngz, nbnd = 20, 20, 20, 4
        assert np.allclose(wvfn.shape, [ngx, ngy, ngz, nbnd])
