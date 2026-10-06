from pathlib import Path

from writeit.compilers.base_compiler import BaseCompiler
from writeit.handlers.chapter_handler import ChapterHandler
from writeit.resolvers.context_resolver import ContextResolver


class ChapteredCompiler(BaseCompiler):

    def update_content(self) -> None:
        if not self.project.is_chaptered:
            raise ValueError("Project is not chaptered!")

        self._content = ""

        context = ContextResolver(self.project).resolve()
        files = self.find_latest_chapters(context)
        handler = ChapterHandler(self.project)

        for file in files:
            self._content += handler.import_content(file)

    def dry_run(self) -> list[Path]:
        """Return the files that would be included in the master file."""
        if not self.project.is_chaptered:
            raise ValueError("Project is not chaptered!")

        context = ContextResolver(self.project).resolve()

        return self.find_latest_chapters(context)
