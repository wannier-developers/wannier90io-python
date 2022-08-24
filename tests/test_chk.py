import itertools
import pathlib

import numpy as np
import pytest

import w90io


@pytest.mark.parametrize('example', ['example01', 'example02'])
def test_read_chk(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.chk.fmt', 'r') as fh:
        chk = w90io.read_chk(fh)
        umn = chk['u_matrix']
        mmn_ref = chk['m_matrix']

    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.nnkp', 'r') as fh:
        nnkp = w90io.parse_nnkp_raw(fh.read())

    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.mmn', 'r') as fh:
        (mmn_test, nnkpts) = w90io.read_mmn(fh)
        nnkpts1 = np.copy(nnkpts)
        nnkpts1[:, :, 0] += 1
        nnkpts1[:, :, 1] += 1

    for (ik, ikb) in itertools.product(range(mmn_test.shape[0]), range(mmn_test.shape[1])):
        mmn_test[ik, ikb] = np.dot(np.dot(umn[ik].conj().T, mmn_test[ik, ikb]), umn[nnkpts[:, :, 1][ik, ikb]])

    assert np.allclose(np.array(nnkp['nnkpts']).reshape(nnkpts.shape), nnkpts1)
    assert np.allclose(mmn_test, mmn_ref)
    assert np.allclose(chk['real_lattice'][0], nnkp['direct_lattice']['a1'])
    assert np.allclose(chk['real_lattice'][1], nnkp['direct_lattice']['a2'])
    assert np.allclose(chk['real_lattice'][2], nnkp['direct_lattice']['a3'])
    assert np.allclose(chk['recip_lattice'][0], nnkp['reciprocal_lattice']['b1'])
    assert np.allclose(chk['recip_lattice'][1], nnkp['reciprocal_lattice']['b2'])
    assert np.allclose(chk['recip_lattice'][2], nnkp['reciprocal_lattice']['b3'])
