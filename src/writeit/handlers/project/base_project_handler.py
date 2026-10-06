from pathlib import Path

from writeit.handlers.base_handler import BaseHandler
from writeit.handlers.part_handler import PartHandler
from writeit.validators.is_folder import IsFolder
from writeit.models.project import Project


class BaseProjectHandler(BaseHandler):

    def __init__(self, base_folder: str | Path):
        super().__init__()
        self._base_folder: Path = IsFolder.validate(base_folder)

    @property
    def project(self) -> Project:
        if self._project is None:
            return self.load()

        return self._project

    def load(self) -> Project:
        """Load the project associated with the base folder."""
        project = Project.load(self._base_folder)
        self._project = project

        return project

    def _add_folder_part(self, part: int) -> None:
        folder = self._get_part_folder(part)

        self._create_folder(folder)
        PartHandler(self.project).create(part)
