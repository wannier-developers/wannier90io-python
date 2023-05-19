import pathlib
import subprocess

import pytest


@pytest.mark.parametrize('example', ['example02'])
def test_cli(wannier90, example):
    if not pathlib.Path(wannier90).name == 'wannier90-3.1.0':
        pytest.skip()

    win_file = pathlib.Path(wannier90)/f'examples/{example}/wannier.win'
    nnkp_file = pathlib.Path(wannier90)/f'examples/{example}/wannier.nnkp'
    wout_file = pathlib.Path(wannier90)/f'examples/{example}/wannier.wout'
    amn_file = pathlib.Path(wannier90)/f'examples/{example}/wannier.amn'
    eig_file = pathlib.Path(wannier90)/f'examples/{example}/wannier.eig'

    assert subprocess.run(['wannier90io', 'parse-win', win_file]).returncode == 0
    assert subprocess.run(['wannier90io', 'parse-nnkp', nnkp_file]).returncode == 0
    assert subprocess.run(['wannier90io', 'parse-wout-iteration-info', wout_file]).returncode == 0
    assert subprocess.run(['wannier90io', 'info-amn', amn_file]).returncode == 0
    assert subprocess.run(['wannier90io', 'info-eig', eig_file]).returncode == 0
