from typing import NamedTuple


class Chapter(NamedTuple):
    context: str
    part: int
    index: int
    version: int
    slug: str
