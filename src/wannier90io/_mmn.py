from __future__ import annotations
import itertools
import typing

import numpy as np


__all__ = ['read_mmn']


def read_mmn(stream: typing.TextIO) -> tuple[np.ndarray, np.ndarray]:
    """
    Read overlaps matrix

    Arguments:
        stream: a file-like stream

    Returns:
        overlaps matrix (Nk, Nn, Nb, Nb)
        nnkps (Nk, Nn, 5)

    """
    stream.readline()   # header

    [Nb, Nk, Nn] = np.fromstring(stream.readline(), sep=' ', dtype=int)

    mmn = np.zeros((Nk, Nn, Nb, Nb), dtype=complex)
    nnkpts = np.zeros((Nk, Nn, 5), dtype=int)

    for (ik, ikb) in itertools.product(range(Nk), range(Nn)):
        nnkpts[ik, ikb] = np.fromstring(stream.readline(), sep=' ', dtype=int)
        mmn[ik, ikb] = np.loadtxt(stream, max_rows=(Nb*Nb)).view(complex).reshape((Nb, Nb), order='F')

    nnkpts[:, :, 0] -= 1
    nnkpts[:, :, 1] -= 1

    return (mmn, nnkpts)
