from writeit.handlers.chapter_handler import ChapterHandler
from writeit.handlers.part_handler import PartHandler
from writeit.resolvers.context_resolver import ContextResolver
from writeit.compilers.base_compiler import BaseCompiler


class PartedCompiler(BaseCompiler):

    def update_content(self) -> None:
        if not self.project.is_parted:
            raise ValueError("Project does not have parts!")

        self._content = ""

        for part in range(1, self.project.parts + 1):
            self._include_files(part)

    def _include_files(self, part: int) -> None:
        context = ContextResolver(self.project).resolve(part)
        files = self.find_latest_chapters(context)

        if not files:
            return None

        first = files.pop(0)

        if not PartHandler.is_part_file(first):
            raise ValueError("Part file not found!")

        self._content += PartHandler(self.project).import_content(part)

        handler = ChapterHandler(self.project)

        for file in files:
            self._content += handler.import_content(file)
