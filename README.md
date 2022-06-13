# Wannier90 I/O with Python

A Python library for reading and writing [Wannier90][w90] files.

## Quickstart

<!--
```python
win_fpath = "./tests/fixtures/wannier90-3.1.0/examples/example01/wannier.win"
nnkp_fpath = "./tests/fixtures/wannier90-3.1.0/examples/example01/wannier.nnkp"
```
-->

<!--pytest-codeblocks:cont-->
```python
import pprint

import w90io


pp = pprint.PrettyPrinter()

with open(win_fpath, 'r') as fh:
    parsed_win = w90io.parse_win_raw(fh.read())

with open(nnkp_fpath, 'r') as fh:
    parsed_nnkp = w90io.parse_nnkp_raw(fh.read())

pp.pprint(parsed_win)
pp.pprint(parsed_nnkp)
```

[w90]: http://wannier.org
