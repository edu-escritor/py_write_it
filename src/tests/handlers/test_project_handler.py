from enums.project_field import ProjectField
from enums.project_type import ProjectType
from handlers.project_handler import ProjectHandler
from models.project import Project
from datetime import date
import pytest


class TestProjectHandler:

    def test_create_standalone_project(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        assert project.title == "The Last Horse"
        assert project.author == "John Smith"
        assert project.is_standalone
        assert (project.root / Project.FILE).is_file()

    def test_create_meta_folder(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        folder = project.root / ProjectHandler.FOLDER_META

        assert folder.is_dir()
        assert folder in project.folders
        assert (folder / handler.FILE_GITKEEP).is_file()

    def test_create_prompts_folder(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        folder = project.root / ProjectHandler.FOLDER_PROMPTS

        assert folder.is_dir()
        assert folder in project.folders
        assert (folder / handler.FILE_GITKEEP).is_file()

    def test_create_standalone_text_folder(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        expected = project.root / handler._translate("files.segments.text")

        assert expected.is_dir()
        assert expected in project.folders

    def test_create_chaptered_project(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.CHAPTERED,
        )

        expected = project.root / handler._translate("files.segments.chapters")

        assert expected.is_dir()
        assert expected in project.folders

    def test_create_parted_project(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.PARTED,
            parts=3,
        )

        name = handler._translate("files.segments.part")

        expected = [
            project.root / f"{name}_01",
            project.root / f"{name}_02",
            project.root / f"{name}_03",
        ]

        for folder in expected:
            assert folder.is_dir()
            assert folder in project.folders
            assert (folder / handler.FILE_GITKEEP).is_file()

    def test_load_project(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        original = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        loaded = ProjectHandler(original.root).load()

        assert loaded.root == original.root
        assert loaded.title == original.title
        assert loaded.author == original.author

    def test_update_author(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        updated = handler.update(
            ProjectField.AUTHOR,
            "Jane Smith",
        )

        assert updated.author == "Jane Smith"

        loaded = Project.load(project.root)

        assert loaded.author == "Jane Smith"

    def test_update_email(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        updated = handler.update(
            ProjectField.EMAIL,
            "jane@example.com",
        )

        assert updated.email == "jane@example.com"

        loaded = Project.load(project.root)

        assert loaded.email == "jane@example.com"

    def test_update_phone(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        updated = handler.update(
            ProjectField.PHONE,
            "987654321",
        )

        assert updated.phone == "987654321"

        loaded = Project.load(project.root)

        assert loaded.phone == "987654321"

    def test_update_loads_project_if_not_loaded(self, tmp_path):
        creator = ProjectHandler(tmp_path)

        project = creator.create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectHandler(project.root)

        updated = handler.update(
            ProjectField.AUTHOR,
            "Jane Smith",
        )

        assert updated.author == "Jane Smith"

        loaded = Project.load(project.root)

        assert loaded.author == "Jane Smith"

    def test_add_part(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.PARTED,
            parts=2,
        )

        updated = handler.add_part()

        name = handler._translate("files.segments.part")
        folder = project.root / f"{name}_03"

        assert updated.parts == 3
        assert folder.is_dir()
        assert folder in updated.folders
        assert (folder / handler.FILE_GITKEEP).is_file()

        loaded = Project.load(project.root)

        assert loaded.parts == 3
        assert folder in loaded.folders

    def test_add_part_to_non_parted_project_raises(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        with pytest.raises(
            RuntimeError,
            match="The project does not have parts!",
        ):
            handler.add_part()

    def test_rename(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

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
        handler = ProjectHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        old_folders = [folder.relative_to(project.root) for folder in project.folders]

        renamed = handler.rename("Where Has the Horse Gone")

        expected = [renamed.root / folder for folder in old_folders]

        assert renamed.folders == expected

        for folder in expected:
            assert folder.is_dir()

    def test_rename_preserves_files(self, tmp_path):
        handler = ProjectHandler(tmp_path)

        project = handler.create(
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
