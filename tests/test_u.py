import pathlib

import numpy as np
import pytest

import wannier90io as w90io


@pytest.mark.parametrize('example', ['example04'])
def test_read_u(wannier90, example):
    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier.win', 'r') as fh:
        win = w90io.parse_win_raw(fh.read())
    nkpt = len(win['kpoints']['kpoints'])
    num_bands = win['parameters']['num_bands']
    num_wann = win['parameters']['num_wann']

    if 'write_u_matrices' not in win['parameters']:
        # an old 2.x version, didn't have write_u_matrices, so skip this test
        # The fixture-making script will already avoid to add the flag in W90 2.x
        pytest.skip("U matrix printing not implemented in Wannier90 2.x")
        return

    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier_u.mat', 'r') as fh:
        (kpts, u_matrices) = w90io.read_u(fh)
    assert np.allclose(kpts, np.asarray(win['kpoints']['kpoints'], dtype=float))
    # Note that the U matrix is num_wann x num_wann, not num_bands x num_wann!
    assert np.allclose(u_matrices.shape, [nkpt, num_wann, num_wann])

    with open(pathlib.Path(wannier90)/f'examples/{example}/wannier_u_dis.mat', 'r') as fh:
        (kpts, u_dis_matrices) = w90io.read_u(fh)
    assert np.allclose(kpts, np.asarray(win['kpoints']['kpoints'], dtype=float))
    assert np.allclose(u_dis_matrices.shape, [nkpt, num_bands, num_wann])
