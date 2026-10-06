from enums.project_field import ProjectField
from handlers.project.project_create_handler import ProjectCreateHandler
from handlers.project.project_update_handler import ProjectUpdateHandler
from models.project import Project


class TestProjectUpdateHandler:

    def test_update_author(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectUpdateHandler(project.root)

        updated = handler.update(
            ProjectField.AUTHOR,
            "Jane Smith",
        )

        assert updated.author == "Jane Smith"

        loaded = Project.load(project.root)

        assert loaded.author == "Jane Smith"

    def test_update_email(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectUpdateHandler(project.root)

        updated = handler.update(
            ProjectField.EMAIL,
            "jane@example.com",
        )

        assert updated.email == "jane@example.com"

        loaded = Project.load(project.root)

        assert loaded.email == "jane@example.com"

    def test_update_phone(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectUpdateHandler(project.root)

        updated = handler.update(
            ProjectField.PHONE,
            "987654321",
        )

        assert updated.phone == "987654321"

        loaded = Project.load(project.root)

        assert loaded.phone == "987654321"

    def test_update_loads_project_if_not_loaded(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectUpdateHandler(project.root)

        updated = handler.update(
            ProjectField.AUTHOR,
            "Jane Smith",
        )

        assert updated.author == "Jane Smith"

        loaded = Project.load(project.root)

        assert loaded.author == "Jane Smith"
