from handlers.project.base_project_handler import BaseProjectHandler
from models.project import Project
from naming.slugifier import Slugifier


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
