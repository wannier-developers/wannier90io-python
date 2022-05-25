from __future__ import annotations
import typing

import numpy as np


__all__ = ['read_eig']


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
