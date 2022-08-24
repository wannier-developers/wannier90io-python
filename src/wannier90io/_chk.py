from __future__ import annotations
import typing

import numpy as np


__all__ = ['read_chk']


def read_chk(stream: typing.TextIO) -> dict:
    """
    Read checkpoint

    Arguments:
        stream: a file-like stream

    Returns:
        dict

    """
    chk = {}

    chk['header'] = stream.readline()
    chk['num_bands'] = Nb = int(stream.readline())
    chk['num_exclude_bands'] = int(stream.readline())
    if chk['num_exclude_bands'] > 0:
        chk['num_exclude_bands'] = np.fromstring(stream.readline(), dtype=int)
    chk['real_lattice'] = np.fromstring(stream.readline(), sep=' ', dtype=float).reshape((3, 3), order='F')
    chk['recip_lattice'] = np.fromstring(stream.readline(), sep=' ', dtype=float).reshape((3, 3), order='F')
    chk['num_kpts'] = Nk = int(stream.readline())
    chk['mp_grid'] = np.fromstring(stream.readline(), sep=' ', dtype=int)
    chk['kpt_latt'] = np.zeros((chk['num_kpts'], 3))
    for idx in range(chk['num_kpts']):
        chk['kpt_latt'][idx] = np.fromstring(stream.readline(), sep=' ', dtype=float)
    chk['nntot'] = Nn = int(stream.readline())
    chk['num_wann'] = Nw = int(stream.readline())
    chk['checkpoint'] = stream.readline()
    chk['have_disentangled'] = bool(int(stream.readline()))
    if chk['have_disentangled']:
        chk['omega_invariant'] = float(stream.readline())
        chk['lwindow'] = np.loadtxt(stream, max_rows=(Nk*Nb), dtype=bool).reshape((Nk, Nb))
        chk['nwindim'] = np.loadtxt(stream, max_rows=Nk, dtype=int)
        chk['u_matrix_opt'] = np.loadtxt(stream, max_rows=(Nk*Nw*Nb), dtype=float).view(complex).reshape((Nk, Nw, Nb))
    chk['u_matrix'] = np.loadtxt(stream, max_rows=(Nk*Nw*Nw), dtype=float).view(complex).reshape((Nw, Nw, Nk), order='F').transpose((2, 0, 1))
    chk['m_matrix'] = np.loadtxt(stream, max_rows=(Nk*Nn*Nw*Nw), dtype=float).view(complex).reshape((Nw, Nw, Nn, Nk), order='F').transpose((3, 2, 0, 1))

    return chk
