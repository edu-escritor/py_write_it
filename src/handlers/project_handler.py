from pathlib import Path
from typing import Final

from enums.locales import Locales
from enums.project_type import ProjectType
from models.project import Project
from validators.is_folder import IsFolder
from .base_handler import BaseHandler
from enums.project_field import ProjectField
from naming.slugifier import Slugifier
from .part_handler import PartHandler


class ProjectHandler(BaseHandler):
    FOLDER_META: Final[str] = "meta"
    FOLDER_PROMPTS: Final[str] = "prompts"

    def __init__(self, base_folder: str | Path):
        super().__init__()
        self._base_folder: Path = IsFolder.validate(base_folder)

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

    def load(self) -> Project:
        """Load the project associated with the base folder."""

        self._project = Project.load(self._base_folder)
        return self.project

    def rename(self, title: str) -> Project:
        """Rename the project and its root folder."""

        project = self._project or self.load()

        old_root = project.root

        project.title = title
        project.slug = Slugifier.slugify(project.title)

        new_root = project.root

        old_root.rename(new_root)

        project.save()

        return project

    def update(
        self,
        field: ProjectField,
        value: str | None,
    ) -> Project:
        """Update a project field and persist the change."""

        project = self._project or self.load()

        setattr(project, field.value, value)
        project.save()

        return project

    def add_part(self) -> Project:
        """Add a new part to a parted project."""

        if not self.project.is_parted:
            raise RuntimeError("The project does not have parts!")

        part = self.project.parts + 1
        self.project.parts = part

        self._add_folder_part(part)

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

    def _add_folder_part(self, part: int) -> None:
        folder = self._get_part_folder(part)

        self._create_folder(folder)
        PartHandler(self.project).create(part)
