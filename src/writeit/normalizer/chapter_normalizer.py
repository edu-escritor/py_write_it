from datetime import date
from pathlib import Path

from writeit.errors.validation_error import ValidationError
from writeit.helpers.finder import Finder
from writeit.models.project import Project
from writeit.parsers.chapter_parser import ChapterParser
from writeit.resolvers.chapter_name_resolver import ChapterNameResolver
from writeit.resolvers.context_resolver import ContextResolver
from writeit.validators.is_valid_file import IsValidFile


class ChapterNormalizer:

    def __init__(self, project: Project):
        self.project: Project = project
        self.resolver: ContextResolver = ContextResolver(self.project)

    def normalize_all(self) -> list[Path]:
        normalized: list[Path] = []

        files = self._find_all()
        if files is None:
            return normalized

        normalized: list[Path] = []
        for file in files:
            handled = self.normalize(file)
            if handled is not None:
                normalized.append(handled)

        return normalized

    def normalize(self, file: Path) -> Path | None:
        try:
            IsValidFile.validate(file)
        except ValidationError:
            return None

        chapter = ChapterParser.parse(file)

        normalized = file.parent / ChapterNameResolver(self.project).resolve(
            version=chapter.version,
            slug=chapter.slug,
            index=chapter.index,
            part=chapter.part,
        )

        if file == normalized:
            return file

        renamed = self._rename(file, normalized)
        self._replace(file, renamed)

        return renamed

    def _replace(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        value = self.project.files.get(source, date.today())

        self.project.remove_file(source)
        self.project.add_file(destination, value)
        self.project.save()

    def _rename(
        self,
        source: Path,
        destination: Path,
    ) -> Path:
        if destination.exists():
            raise FileExistsError(
                f"'{self.project.contextualized_path(source)}' would be normalized to '{self.project.contextualized_path(destination)}' but it already exists!"
            )

        return source.rename(destination)

    def _find_all(self) -> list[Path] | None:
        found = self._find_all_standalone()
        if found is not None:
            return found

        found = self._find_all_chaptered()
        if found is not None:
            return found

        return self._find_all_parted()

    def _find_all_standalone(self) -> list[Path] | None:
        if not self.project.is_standalone:
            return None

        return Finder.find_all(folder=self.resolver.resolve())

    def _find_all_chaptered(self) -> list[Path] | None:
        if not self.project.is_chaptered:
            return None

        return Finder.find_all(folder=self.resolver.resolve())

    def _find_all_parted(self) -> list[Path] | None:
        if not self.project.is_parted:
            return None

        files: list[Path] = []

        for part in range(1, self.project.parts + 1):
            folder = self.resolver.resolve(part)
            files.extend(Finder.find_all(folder))

        files.sort()

        return files
