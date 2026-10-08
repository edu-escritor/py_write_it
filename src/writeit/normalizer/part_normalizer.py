from pathlib import Path

from writeit.errors.validation_error import ValidationError
from writeit.helpers.segment_formatter import SegmentFormatter
from writeit.models.project import Project
from writeit.parsers.part_parser import PartParser
from writeit.validators.is_valid_part_file import IsValidPartFile


class PartNormalizer:

    def __init__(self, project: Project):
        self.project = project

    def normalize_all(self) -> list[Path]:
        normalized: list[Path] = []

        if not self.project.is_parted:
            return normalized

        index = SegmentFormatter.index(value=0, allow_zero=True)

        for part in range(1, self.project.parts + 1):
            folder = self.project.root / SegmentFormatter.part_slug(
                value=part,
                locale=self.project.locale,
                connector="_",
            )

            for file in folder.glob(f"*{index}*.md"):
                handled = self.normalize(file)

                if handled is not None:
                    normalized.append(handled)

        return normalized

    def normalize(self, file: Path) -> Path | None:
        try:
            IsValidPartFile.validate(file)
        except ValidationError:
            return None

        part = PartParser.parse(file)

        normalized = file.parent / SegmentFormatter.part_filename(
            value=part.part,
            locale=self.project.locale,
        )

        if file == normalized:
            return file

        return self._rename(file, normalized)

    def _rename(self, source: Path, destination: Path) -> Path:
        return source.rename(destination)
