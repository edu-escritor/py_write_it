from pathlib import Path

from writeit.models.project import Project
from writeit.normalizer.chapter_normalizer import ChapterNormalizer
from writeit.normalizer.part_normalizer import PartNormalizer
from writeit.parsers.root_parser import RootParser


class FileNormalizeHandler:
    def __init__(self, folder: Path) -> None:
        self._project: Project = Project.load(RootParser.parse(folder))

    def normalize(self) -> list[Path]:
        files = ChapterNormalizer(self._project).normalize_all()

        if self._project.is_parted:
            files.extend(PartNormalizer(self._project).normalize_all())

        return files
