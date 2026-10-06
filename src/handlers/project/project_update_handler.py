from enums.project_field import ProjectField
from handlers.project.base_project_handler import BaseProjectHandler
from models.project import Project


class ProjectUpdateHandler(BaseProjectHandler):

    def update(
        self,
        field: ProjectField,
        value: str | None,
    ) -> Project:
        """Update a project field and persist the change."""
        setattr(self.project, field.value, value)
        self.project.save()

        return self.project
