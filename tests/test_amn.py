import pathlib

import numpy as np
import pytest
import w90io


@pytest.mark.parametrize('example', ['example01', 'example02', 'example03', 'example04'])
def test_read_amn(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.amn', 'r') as fh:
        amn = w90io.read_amn(fh)

        fh.seek(0)
        fh.readline()
        [Nb, Nk, Np] = np.fromstring(fh.readline(), sep=' ', dtype=int)

        assert amn.shape == (Nk, Nb, Np)

        for line in fh.readlines():
            [m_idx, n_idx, k_idx, a1, a2] = np.fromstring(line, sep=' ')
            k_idx = int(k_idx) - 1
            m_idx = int(m_idx) - 1
            n_idx = int(n_idx) - 1

            assert(abs(amn[k_idx, m_idx, n_idx] - (a1+1j*a2)) < 1e-12)


@pytest.mark.parametrize('example', ['example02', 'example03', 'example04'])
def test_write_amn(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.amn', 'r') as fh:
        amn_ref = w90io.read_amn(fh)

    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier1.amn', 'w+') as fh:
        w90io.write_amn(fh, amn_ref)

        fh.seek(0)
        amn_test = w90io.read_amn(fh)

    assert np.allclose(amn_test, amn_ref)
