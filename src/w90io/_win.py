from __future__ import annotations
import re


patterns = {
    'comment': re.compile(
        r'(!|#)[ \t]*(?P<comment>.+)\n',
    ),
    'parameter': re.compile(
        r'^[ \t]*(?!begin|end)(?P<parameter>\w+)[ \t]*[ =:][ \t]*(?P<value>[\S ]+)[ \t]*$',
        re.IGNORECASE | re.MULTILINE
    ),
    'block': re.compile(
        r'[ \t]*begin[ \t]+(?P<block>\w+)(?P<contents>.+)\s+end[ \t]+(?P=block)',
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
}


def convert(string: str) -> int | float | bool | str:
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
    elif len(re.split('[ ,]', string)) > 1 and '-' not in string:
        return list(map(int, re.split('[ ,]', string)))
    else:
        return string


def extract_comments(string: str) -> list[str]:
    return [
        match.group().strip()
        for match in re.finditer(patterns['comment'], string)
    ]


def extract_parameters(string: str) -> list[str] :
    string = re.sub(patterns['comment'], '', string)
    string = re.sub(patterns['block'], '', string)

    return [
        match.group().strip()
        for match in re.finditer(patterns['parameter'], string)
    ]


def extract_blocks(string: str) -> list[str]:
    string = re.sub(patterns['comment'], '', string)

    return [
        match.group().strip()
        for match in re.finditer(patterns['block'], string)
    ]


def parse_parameters(parameters: list[str]) -> dict:
    return {
        match.group('parameter'): convert(match.group('value'))
        for match in map(patterns['parameter'].match, parameters)
    }


def parse_blocks(blocks: list[str]) -> list[dict]:
    return {
        match.group('block'): match.group('contents').strip()
        for match in map(patterns['block'].match, blocks)
    }
