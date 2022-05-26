from __future__ import annotations
import typing
import re

from . import _core


patterns = {
    'convergence_line': re.compile(
        r'^\s*'
        r'(?P<iter>\d+)\s+'
        rf'(?P<delta>{_core.expressions["float"]})\s+'
        rf'(?P<gradient>{_core.expressions["float"]})\s+'
        rf'(?P<spread>{_core.expressions["float"]})\s+'
        rf'(?P<time>{_core.expressions["float"]})'
        rf'\s*<-- CONV$'
    ),
    'spread_line': re.compile(
        r'^\s*'
        rf'O_D=\s*(?P<omega_d>{_core.expressions["float"]})\s+'
        rf'O_OD=\s*(?P<omega_od>{_core.expressions["float"]})\s+'
        rf'O_TOT=\s*(?P<omega_tot>{_core.expressions["float"]})'
        rf'\s*<-- SPRD$'
    ),
    'delta_line': re.compile(
        r'^ Delta:\s*'
        rf'O_D=\s*(?P<omega_d>{_core.expressions["float"]})\s+'
        rf'O_OD=\s*(?P<omega_od>{_core.expressions["float"]})\s+'
        rf'O_TOT=\s*(?P<omega_tot>{_core.expressions["float"]})'
        rf'\s*<-- DLTA$'
    ),
    'disentanglement_line': re.compile(
        r'^\s*'
        r'(?P<iter>\d+)\s+'
        rf'(?P<omega_i_i>{_core.expressions["float"]})\s+'
        rf'(?P<omega_i_f>{_core.expressions["float"]})\s+'
        rf'(?P<delta>{_core.expressions["float"]})\s+'
        rf'(?P<time>{_core.expressions["float"]})'
        rf'\s*<-- DIS$'
    ),
}


def parse_iteration_info(stream: typing.TextIO) -> dict:
    convergence = []
    spread = []
    delta = []
    disentanglement = []
    for line in stream.readlines():
        match = patterns['convergence_line'].match(line)
        if match is not None:
            convergence += [{
                'iter': int(match.group('iter')),
                'delta': float(match.group('delta')),
                'gradient': float(match.group('gradient')),
                'spread': float(match.group('spread')),
                'time': float(match.group('time')),
            }]

        match = patterns['spread_line'].match(line)
        if match is not None:
            spread += [{
                'omega_d': float(match.group('omega_d')),
                'omega_od': float(match.group('omega_od')),
                'omega_tot': float(match.group('omega_tot')),
            }]

        match = patterns['delta_line'].match(line)
        if match is not None:
            delta += [{
                'omega_d': float(match.group('omega_d')),
                'omega_od': float(match.group('omega_od')),
                'omega_tot': float(match.group('omega_tot')),
            }]

        match = patterns['disentanglement_line'].match(line)
        if match is not None:
            disentanglement += [{
                'iter': int(match.group('iter')),
                'omega_i_i': float(match.group('omega_i_i')),
                'omega_i_f': float(match.group('omega_i_f')),
                'delta': float(match.group('delta')),
                'time': float(match.group('time')),
            }]

    return {
        'convergence': convergence,
        'spread': spread,
        'delta': delta,
        'disentanglement': disentanglement,
    }


def parse_wout(stream: typing.IO) -> dict:
    pass
