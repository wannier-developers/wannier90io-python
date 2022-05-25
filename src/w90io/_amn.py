from __future__ import annotations
import typing

import numpy as np


__all__ = ['read_amn']


def read_amn(stream: typing.TextIO) -> np.ndarray:
    """
    Read projections matrix

    Arguments:
        stream: a file-like stream

    Returns:
        projections matrix (Nk, Nb, Np)

    """
    stream.readline()

    [Nb, Nk, Np] = np.fromstring(stream.readline(), sep=' ', dtype=int)

    raw_data = np.loadtxt(stream).reshape((Nk, Np, Nb, 5))

    amn = np.transpose(raw_data[:, :, :, 3] + 1j*raw_data[:, :, :, 4], axes=(0, 2, 1))

    return amn
