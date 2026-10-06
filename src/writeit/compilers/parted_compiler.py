from pathlib import Path

from writeit.compilers.base_compiler import BaseCompiler
from writeit.handlers.chapter_handler import ChapterHandler
from writeit.handlers.part_handler import PartHandler
from writeit.resolvers.context_resolver import ContextResolver


class PartedCompiler(BaseCompiler):

    def update_content(self) -> None:
        if not self.project.is_parted:
            raise ValueError("Project does not have parts!")

        self._content = ""

        for part in range(1, self.project.parts + 1):
            self._include_files(part)

    def dry_run(self) -> list[Path]:
        """Return the files that would be included in the master file."""
        result: list[Path] = []

        for part in range(1, self.project.parts + 1):
            context = ContextResolver(self.project).resolve(part)

            part_file = PartHandler(self.project).create_file_name(part)

            if part_file is not None:
                result.append(part_file)

            result.extend(self.find_latest_chapters(context))

        return result

    def _include_files(self, part: int) -> None:
        context = ContextResolver(self.project).resolve(part)
        files = self.find_latest_chapters(context)

        if not files:
            return None

        self._content += PartHandler(self.project).import_content(part)

        handler = ChapterHandler(self.project)

        for file in files:
            self._content += handler.import_content(file)
        return None
