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
