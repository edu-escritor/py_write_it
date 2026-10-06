from pathlib import Path

from writeit.compilers.base_compiler import BaseCompiler
from writeit.resolvers.chapter_name_resolver import ChapterNameResolver
from writeit.resolvers.context_resolver import ContextResolver
from writeit.resolvers.version_resolver import VersionResolver


class StandaloneCompiler(BaseCompiler):

    def update_content(self) -> None:
        if not self.project.is_standalone:
            raise ValueError("Project is not standalone!")

        self._content = self._latest_file_name().read_text(encoding="utf-8").strip()

    def dry_run(self) -> list[Path]:
        """Return the files that would be included in the master file."""
        if not self.project.is_standalone:
            raise ValueError("Project is not standalone!")

        return [self._latest_file_name()]

    def _latest_file_name(self) -> Path:
        folder = ContextResolver(self.project).resolve()

        file = ChapterNameResolver(self.project).resolve(
            version=1,
            title=self.project.title,
        )

        version = VersionResolver(self.project).resolve(folder / file)

        return folder / ChapterNameResolver(self.project).resolve(
            version=version,
            title=self.project.title,
        )
