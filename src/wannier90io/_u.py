from __future__ import annotations
import typing

import numpy as np

# TODO: implement also read_u_dis
__all__ = ['read_u']


def read_u(stream: typing.TextIO) -> tuple[np.ndarray, np.ndarray]:
    """
    Read unitary matrix file (seedname_u.mat) or the rectangular U_dis matrix
    file (seedname_u_dis.mat).

    Note:
        for the _u.mat file, num_bands == num_wann.

    Arguments:
        stream: a file-like stream

    Returns:
        kpoint coordinates in fractional coordinates (num_kpts, 3)
        U matrix U(k) or U_dis(k) (num_kpts, num_bands, num_wann)

    """
    stream.readline()   # header

    [nkpt, num_wann, num_bands] = np.fromstring(stream.readline(), sep=' ', dtype=int)
    u_matrices = np.zeros((nkpt, num_bands, num_wann), dtype=complex)
    kpoints = []

    for ikpt in range(nkpt):
        empty = stream.readline()   # header
        assert not empty.strip(), f"Expected empty line but found instead: '{empty}'"

        kpoint = np.fromstring(stream.readline(), sep=' ', dtype=float)
        assert len(kpoint) == 3
        kpoints.append(kpoint)
        u_matrices[ikpt, :, :] = np.loadtxt(stream, max_rows=(num_wann * num_bands)).view(complex).reshape((num_bands, num_wann), order='F')

    return np.array(kpoints), u_matrices
