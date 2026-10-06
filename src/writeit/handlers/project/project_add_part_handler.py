from writeit.handlers.project.base_project_handler import BaseProjectHandler
from writeit.models.project import Project


class ProjectAddPartHandler(BaseProjectHandler):
    def add_part(self) -> Project:
        """Add a new part to a parted project."""

        if not self.project.is_parted:
            raise RuntimeError("The project does not have parts!")

        part = self.project.parts + 1
        self.project.parts = part

        # _add_folder_part() persists the project.
        self._add_folder_part(part)

        return self.project
