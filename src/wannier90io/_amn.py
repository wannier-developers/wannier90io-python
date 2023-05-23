from __future__ import annotations
import typing

import numpy as np


__all__ = ['read_amn', 'write_amn']


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


def write_amn(stream: typing.TextIO, amn: np.ndarray, header: typing.Optional[str] = 'HEADER'):
    r"""
    Write projections matrix

    Arguments:
        stream: a file-like stream
        amn: projections matrix (Nk, Nb, Np)
        header: header

    """
    (Nk, Nb, Np) = amn.shape
    indices = np.mgrid[:Nb, :Np, :Nk].reshape((3, -1), order='F') + 1

    amn = np.transpose(amn, axes=(1, 2, 0)).flatten(order='F').view(float).reshape((-1, 2))
    data = np.column_stack((indices.T, amn))

    print(header, file=stream)
    print(f'{Nb:12d}{Nk:12d}{Np:12d}', file=stream)
    np.savetxt(stream, data, fmt='%5d%5d%5d%18.12f%18.12f')
