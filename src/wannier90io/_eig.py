from __future__ import annotations
import typing

import numpy as np


__all__ = ['read_eig', 'write_eig']


def read_eig(stream: typing.TextIO) -> np.ndarray:
    """
    Read eigenvalues matrix

    Arguments:
        stream: a file-like stream

    Returns:
        eigenvalues matrix (Nk, Nb)

    """
    raw_data = np.loadtxt(stream)

    Nb = int(raw_data[-1, 0])
    Nk = int(raw_data[-1, 1])

    eig = raw_data[:, 2].reshape((Nk, Nb))

    return eig


def write_eig(stream: typing.TextIO, eig: np.ndarray):
    r"""
    Write eigenvalues matrix

    Arguments:
        stream: a file-like stream
        eig: eigenvalues matrix (Nk, Nb)

    """
    (Nk, Nb) = eig.shape
    indices = np.mgrid[:Nb, :Nk].reshape((2, Nk*Nb), order='F') + 1

    data = np.column_stack((indices.T, eig.flatten()))

    np.savetxt(stream, data, fmt='%5d%5d%18.12f')
