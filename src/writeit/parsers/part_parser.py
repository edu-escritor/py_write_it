import re
from pathlib import Path

from writeit.models.part import Part
from writeit.validators.is_valid_part_file import IsValidPartFile


class PartParser:

    @staticmethod
    def parse(path: Path) -> Part:
        file = IsValidPartFile.validate(path)

        pattern = r"^p(?P<part>\d+)_" r"i(?P<index>\d+)_" r"(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)" r"\.md$"

        match = re.fullmatch(pattern, file.name)

        if not match:
            raise ValueError(f"Invalid file path: {path}")

        return Part(
            context=file.parent.name,
            part=int(match.group("part")),
            index=int(match.group("index")),
            slug=match.group("slug"),
        )
