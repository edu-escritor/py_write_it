import shutil
from datetime import date
from pathlib import Path

from handlers.base_handler import BaseHandler
from models.chapter import Chapter
from parsers.chapter_parser import ChapterParser
from resolvers.chapter_name_resolver import ChapterNameResolver
from resolvers.index_resolver import IndexResolver
from resolvers.version_resolver import VersionResolver


class ChapterHandler(BaseHandler):

    def create(
        self,
        title: str,
        part: int = 0,
    ) -> Path:
        """Creates a new chapter file."""
        folder = self._get_context_folder(part)

        index = IndexResolver(self.project).next(folder)

        file_name = ChapterNameResolver(self.project).resolve(
            title=title,
            version=1,
            index=index,
            part=part,
        )

        file = folder / file_name

        content = self._create_content(title)
        file.write_text(
            content + "\n",
            encoding="utf-8",
        )

        self.project.add_file(
            file,
            date.today(),
        )
        self.project.save()

        return file

    def create_version(
        self,
        file: Path,
        title: str | None = None,
    ) -> Path:
        """Creates a new version of a chapter file."""
        chapter = ChapterParser.parse(file)

        source_file = self._source_file_name(
            chapter=chapter,
            file=file,
        )
        destination_file = self._destination_file_name(
            chapter=ChapterParser.parse(source_file),
            title=title,
            file=source_file,
        )

        self._copy_file(
            source_file=source_file,
            destination_file=destination_file,
            title=title,
        )

        self.project.add_file(
            destination_file,
            date.today(),
        )
        self.project.save()

        return destination_file

    def _copy_file(
        self,
        source_file: Path,
        destination_file: Path,
        title: str | None,
    ) -> None:
        if title is None:
            shutil.copy(source_file, destination_file)
            return

        content = source_file.read_text(encoding="utf-8").strip()

        lines = content.splitlines()
        lines[0] = f"# {title.strip()}"

        destination_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _source_file_name(self, chapter: Chapter, file: Path) -> Path:
        version = VersionResolver(self.project).resolve(file)
        resolver = ChapterNameResolver(self.project)
        file_name = resolver.resolve(version=version, slug=chapter.slug, index=chapter.index, part=chapter.part)
        return file.parent / file_name

    def _destination_file_name(self, chapter: Chapter, title: str | None, file: Path) -> Path:
        version = VersionResolver(self.project).resolve(file) + 1
        resolver = ChapterNameResolver(self.project)

        if title is not None:
            file_name = resolver.resolve(version=version, title=title, index=chapter.index, part=chapter.part)
        else:
            file_name = resolver.resolve(version=version, slug=chapter.slug, index=chapter.index, part=chapter.part)
        return file.parent / file_name

    def _create_content(self, title: str) -> str:
        values: dict[str, str] = {"title": title.strip()}

        return self.render_template(
            "create/chapter.md.j2",
            values,
        ).strip()
