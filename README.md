# Wannier90 I/O with Python

A Python library for reading and writing [Wannier90][w90] files.

## Quickstart

```python
import pprint

import w90io


pp = pprint.PrettyPrinter()

with open('wannier.win', 'r') as fh:
    parsed_win = w90io.parse_win(fh.read())

with open('wannier.nnkp', 'r') as fh:
    parsed_nnkp = w90io.parse_nnkp(fh.read())

pp.pprint(parsed_win)
pp.pprint(parsed_nnkp)
```

[w90]: http://wannier.org
