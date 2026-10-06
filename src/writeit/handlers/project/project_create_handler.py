from typing import Final

from writeit.handlers.chapter_handler import ChapterHandler
from writeit.handlers.project.base_project_handler import BaseProjectHandler
from writeit.enums.project_type import ProjectType
from writeit.enums.locales import Locales
from writeit.models.project import Project


class ProjectCreateHandler(BaseProjectHandler):
    FOLDER_META: Final[str] = "meta"
    FOLDER_PROMPTS: Final[str] = "prompts"

    def create(
        self,
        title: str,
        author: str,
        project_type: ProjectType = ProjectType.STANDALONE,
        parts: int = 0,
        locale: Locales = Locales.PORTUGUESE_EUROPEAN,
        email: str | None = None,
        phone: str | None = None,
    ) -> Project:
        """Create a new project and its initial folder structure."""

        self._project = Project(
            base_folder=self._base_folder,
            title=title,
            author=author,
            project_type=project_type,
            parts=parts,
            locale=locale,
            email=email,
            phone=phone,
        )

        self.project.save()

        self._add_folder_meta()
        self._add_folder_prompts()
        self._add_folder_text()
        self._add_folder_chapters()
        self._add_folder_parts()

        return self.project

    def _add_folder_meta(self) -> None:
        folder = self.project.root / self.FOLDER_META
        self._create_folder(folder)

    def _add_folder_prompts(self) -> None:
        folder = self.project.root / self.FOLDER_PROMPTS
        self._create_folder(folder)

    def _add_folder_text(self) -> None:
        if not self.project.is_standalone:
            return

        folder = self.project.root / self._translate("files.segments.text")

        self._create_folder(folder)
        file = ChapterHandler(self.project).create(self.project.title)

    def _add_folder_chapters(self) -> None:
        if not self.project.is_chaptered:
            return

        folder = self.project.root / self._translate("files.segments.chapters")

        self._create_folder(folder)

    def _add_folder_parts(self) -> None:
        if not self.project.is_parted:
            return

        for part in range(1, self.project.parts + 1):
            self._add_folder_part(part)
