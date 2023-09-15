import pathlib

import numpy as np
import pytest

import wannier90io as w90io


@pytest.mark.parametrize('example', ['example01', 'example02', 'example04'])
def test_read_mmn(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.mmn', 'r') as fh:
        (mmn, nnkpts) = w90io.read_mmn(fh)
        nnkpts[:, :, 0] += 1
        nnkpts[:, :, 1] += 1

    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.nnkp', 'r') as fh:
        nnkp = w90io.parse_nnkp_raw(fh.read())

    assert np.allclose(nnkpts, np.asarray(nnkp['nnkpts'], dtype=int).reshape(nnkpts.shape))
