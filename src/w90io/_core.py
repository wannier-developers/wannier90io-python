from __future__ import annotations
import re


expressions = {
    'float': r'[-+]?(\d+(\.\d*)?|\.\d+)([eEdD][-+]?\d+)?',
    '3-vector': (
        r'[-+]?(\d+(\.\d*)?|\.\d+)([eEdD][-+]?\d+)?[ \t]+'
        r'[-+]?(\d+(\.\d*)?|\.\d+)([eEdD][-+]?\d+)?[ \t]+'
        r'[-+]?(\d+(\.\d*)?|\.\d+)([eEdD][-+]?\d+)?'
    ),
}

patterns = {
    'comment': re.compile(
        r'(!|#)[ \t]*(?P<comment>.+)\n',
    ),
    'parameter': re.compile(
        r'^[ \t]*(?!begin|end)(?P<parameter>\w+)[ \t]*[ =:][ \t]*(?P<value>[\S ]+)[ \t]*$',
        re.IGNORECASE | re.MULTILINE
    ),
    'block': re.compile(
        r'[ \t]*begin[ \t]+(?P<block>\w+)\s+(?P<contents>.+\n)[ \t]*end[ \t]+(?P=block)',
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    ),
}


def convert(string: str) -> int | float | bool | str | list[int] | list[float]:
    string = string.strip()

    # regular expressions adapted (in part) from:
    # https://docs.python.org/3/library/re.html#simulating-scanf
    if re.compile(r'^[-+]?\d+$').match(string):
        return int(string)
    elif re.compile(r'^[-+]?(\d+(\.\d*)?|\.\d+)([eEdD][-+]?\d+)?$').match(string):
        return float(string.replace('d', 'e').replace('D', 'e'))
    elif re.compile(r'^t|true|[.]true[.]$', re.IGNORECASE).match(string):
        return True
    elif re.compile(r'^f|false|[.]false[.]$', re.IGNORECASE).match(string):
        return False
    elif re.compile(rf'^{expressions["3-vector"]}$').match(string):
        try:
            return list(map(int, re.split('[ ,]', string)))
        except ValueError:
            return list(map(float, re.split('[ ,]', string)))
    elif re.compile(r'^\d+(-\d+)?([ \t,;]+\d+(-\d+)?)+$').match(string):
        values = []
        for component in re.split('[ \t,;]', string):
            if '-' in component:
                [i1, i2] = list(map(int, component.split('-')))
                values += list(range(i1, i2+1))
            else:
                values.append(int(component))
        return values
    else:
        return string


def extract_comments(string: str) -> list[str]:
    return [
        match.group()
        for match in re.finditer(patterns['comment'], string)
    ]


def extract_parameters(string: str) -> list[str] :
    string = re.sub(patterns['comment'], '', string)
    string = re.sub(patterns['block'], '', string)

    return [
        match.group()
        for match in re.finditer(patterns['parameter'], string)
    ]


def extract_blocks(string: str) -> list[str]:
    string = re.sub(patterns['comment'], '', string)

    return [
        match.group()
        for match in re.finditer(patterns['block'], string)
    ]


def parse_parameters(parameters: list[str]) -> dict:
    return {
        match.group('parameter'): convert(match.group('value'))
        for match in map(patterns['parameter'].match, parameters)
    }


def parse_blocks(blocks: list[str]) -> list[dict]:
    return {
        match.group('block').lower(): match.group('contents')
        for match in map(patterns['block'].match, blocks)
    }
