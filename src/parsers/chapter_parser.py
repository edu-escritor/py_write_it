import re
from pathlib import Path

from models.chapter import Chapter
from validators.is_valid_file import IsValidFile


class ChapterParser:

    @staticmethod
    def parse(path: Path) -> Chapter:
        file = IsValidFile.validate(path)

        pattern = (
            r"^(?:p(?P<part>\d{3})_)?"
            r"(?:i(?P<index>\d{4})_)?"
            r"v(?P<version>\d{3})_"
            r"(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)"
            r"\.md$"
        )
        match = re.fullmatch(pattern, file.name)

        if not match:
            raise ValueError(f"Invalid file path: {path}")

        return Chapter(
            context=file.parent.name,
            part=(int(match.group("part")) if match.group("part") else 0),
            index=(int(match.group("index")) if match.group("index") else 0),
            version=int(match.group("version")),
            slug=match.group("slug"),
        )
