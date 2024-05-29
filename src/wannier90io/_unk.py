from __future__ import annotations
import typing

import numpy as np

# TODO: implement also read_unk_unformatted (that is the default)
__all__ = ['read_unk_formatted']


def read_unk_formatted(stream: typing.TextIO) -> tuple[int, np.ndarray]:
    """
    Read wavefunction files (UNKnnnnn.n files) in formatted format.

    Note that the UNK files must have been created using the `wvfn_formatted`
    option set to True in the interface code (e.g. pw2wannier90.x for the
    Quantum ESPRESSO interface). Note that this is *not* the default, however
    for reading into an external code, this is recommended for portability.

    Note:
       for now only works in the non-spinor case.
       Spinor case still to be implemented.

    Arguments:
        stream: a file-like stream

    Returns:
        k-point index ik (integer)
        complex wavefunction (ngx, ngy, ngz, Nb)

    """
    [ngx, ngy, ngz, ik, nbnd] = np.fromstring(stream.readline(), sep=' ', dtype=int)

    wvfn = np.zeros((ngx, ngy, ngz, nbnd), dtype=complex)

    for ibnd in range(nbnd):
        wvfn[:, :, :, ibnd] = np.loadtxt(stream, max_rows=(ngx * ngy * ngz)).view(complex).reshape((ngx, ngy, ngz), order='F')

    return (ik, wvfn)
