import os
import shutil

import pytest


example_ids = {
    'wannier90-2.0.1': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20],
    'wannier90-2.1':   [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20],
    'wannier90-3.0.0': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20],
    'wannier90-3.1.0': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 17, 18, 19, 20],
}


@pytest.fixture(scope='session', params=example_ids.keys())
def wannier90(request, tmpdir_factory):
    wannier90 = os.path.join(os.path.dirname(__file__), './fixtures')
    for example_dir in [f'{request.param}/examples/example{i:02d}' for i in example_ids[request.param]]:
        shutil.copytree(os.path.join(wannier90, example_dir), os.path.join(str(tmpdir_factory.getbasetemp()), example_dir))

    return os.path.join(str(tmpdir_factory.getbasetemp()), request.param)
