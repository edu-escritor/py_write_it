from writeit.handlers.project.base_project_handler import BaseProjectHandler
from writeit.naming.slugifier import Slugifier
from writeit.models.project import Project


class ProjectRenameHandler(BaseProjectHandler):
    def rename(self, title: str) -> Project:
        """Rename the project and its root folder."""
        old_root = self.project.root

        self.project.title = title
        self.project.slug = Slugifier.slugify(self.project.title)

        new_root = self.project.root

        old_root.rename(new_root)

        self.project.save()

        return self.project
