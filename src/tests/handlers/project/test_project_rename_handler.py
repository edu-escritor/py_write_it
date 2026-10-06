from datetime import date

from writeit.handlers.project.project_create_handler import ProjectCreateHandler
from writeit.handlers.project.project_rename_handler import ProjectRenameHandler
from writeit.models.project import Project


class TestProjectRenameHandler:

    def test_rename(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectRenameHandler(project.root)

        old_root = project.root

        renamed = handler.rename("Where Has the Horse Gone")

        new_root = tmp_path / "where-has-horse-gone"

        assert renamed.title == "Where Has the Horse Gone"
        assert renamed.slug == "where-has-horse-gone"
        assert renamed.root == new_root

        assert not old_root.exists()
        assert new_root.is_dir()
        assert (new_root / Project.FILE).is_file()

        loaded = Project.load(new_root)

        assert loaded.title == "Where Has the Horse Gone"
        assert loaded.slug == "where-has-horse-gone"
        assert loaded.root == new_root

    def test_rename_preserves_folders(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        old_folders = [folder.relative_to(project.root) for folder in project.folders]

        handler = ProjectRenameHandler(project.root)

        renamed = handler.rename("Where Has the Horse Gone")

        expected = [renamed.root / folder for folder in old_folders]

        assert renamed.folders == expected

        for folder in expected:
            assert folder.is_dir()

    def test_rename_preserves_files(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        file = project.root / "test.md"
        file.write_text(
            "Test",
            encoding="utf-8",
        )

        project.add_file(
            file,
            date(2026, 10, 5),
        )
        project.save()

        handler = ProjectRenameHandler(project.root)

        renamed = handler.rename("Where Has the Horse Gone")

        renamed_file = renamed.root / "test.md"

        assert renamed_file.is_file()
        assert renamed_file in renamed.files
        assert renamed.files[renamed_file] == date(
            2026,
            10,
            5,
        )

        loaded = Project.load(renamed.root)

        assert renamed_file in loaded.files
