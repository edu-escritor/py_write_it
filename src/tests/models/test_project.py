import json
from datetime import date

import pytest

from writeit.enums.project_type import ProjectType
from writeit.enums.locales import Locales
from writeit.errors.validation_error import ValidationError
from writeit.models.project import Project


class TestProject:

    def test_create_default_project(self, tmp_path):
        project = Project(base_folder=tmp_path)

        assert project.base_folder == tmp_path
        assert project.title == Project.DEFAULT_TITLE
        assert project.slug == "write-it"
        assert project.project_type == ProjectType.STANDALONE
        assert project.parts == 0
        assert project.locale == Locales.PORTUGUESE_EUROPEAN
        assert project.author == Project.DEFAULT_AUTHOR
        assert project.email is None
        assert project.phone is None
        assert project.created_at == date.today()
        assert project.updated_at is None
        assert project.folders == []
        assert project.files == {}

    def test_create_project(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            slug="last-horse",
            project_type=ProjectType.PARTED,
            parts=3,
            locale=Locales.PORTUGUESE_EUROPEAN,
            author="John Smith",
            email="john@example.com",
            phone="123456789",
            created_at=date(2026, 10, 1),
            updated_at=date(2026, 10, 3),
            folders=["notes", "chapters"],
            files={
                "notes.md": date(2026, 10, 2),
                "master.md": date(2026, 10, 3),
            },
        )

        assert project.title == "The Last Horse"
        assert project.slug == "last-horse"
        assert project.project_type == ProjectType.PARTED
        assert project.parts == 3
        assert project.author == "John Smith"
        assert project.created_at == date(2026, 10, 1)
        assert project.updated_at == date(2026, 10, 3)

    def test_slug_is_generated_from_title(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
        )

        assert project.slug == "last-horse"

    def test_custom_slug_is_preserved(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            slug="horse",
        )

        assert project.slug == "horse"

    def test_root(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
        )

        assert project.root == tmp_path / "last-horse"

    def test_folders_are_sorted(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            folders=["zeta", "alpha", "beta"],
        )

        assert project.folders == [
            project.root / "alpha",
            project.root / "beta",
            project.root / "zeta",
        ]

    def test_add_folder(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            folders=["beta", "delta"],
        )

        project.add_folder("alpha")

        assert project.folders == [
            project.root / "alpha",
            project.root / "beta",
            project.root / "delta",
        ]

    def test_add_existing_folder_does_nothing(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            folders=["alpha"],
        )

        project.add_folder("alpha")

        assert project.folders == [
            project.root / "alpha",
        ]

    def test_remove_folder(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            folders=["alpha", "beta"],
        )

        project.remove_folder("alpha")

        assert project.folders == [
            project.root / "beta",
        ]

    def test_remove_nonexistent_folder_does_nothing(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            folders=["alpha"],
        )

        project.remove_folder("beta")

        assert project.folders == [
            project.root / "alpha",
        ]

    def test_files_are_sorted(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            files={
                "zeta.md": date(2026, 10, 3),
                "alpha.md": date(2026, 10, 1),
                "beta.md": date(2026, 10, 2),
            },
        )

        assert list(project.files) == [
            project.root / "alpha.md",
            project.root / "beta.md",
            project.root / "zeta.md",
        ]

    def test_add_file(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            files={
                "beta.md": date(2026, 10, 2),
            },
        )

        project.add_file(
            "alpha.md",
            date(2026, 10, 1),
        )

        assert list(project.files) == [
            project.root / "alpha.md",
            project.root / "beta.md",
        ]

        assert project.files[project.root / "alpha.md"] == date(2026, 10, 1)

    def test_add_existing_file_does_not_replace_date(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            files={
                "master.md": date(2026, 10, 1),
            },
        )

        project.add_file(
            "master.md",
            date(2026, 10, 3),
        )

        assert project.files[project.root / "master.md"] == date(2026, 10, 1)

    def test_remove_file(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            files={
                "master.md": date(2026, 10, 1),
            },
        )

        project.remove_file("master.md")

        assert project.files == {}

    def test_remove_nonexistent_file_does_nothing(self, tmp_path):
        project = Project(base_folder=tmp_path)

        project.remove_file("master.md")

        assert project.files == {}

    def test_project_type_properties(self, tmp_path):
        standalone = Project(
            base_folder=tmp_path,
            project_type=ProjectType.STANDALONE,
        )

        chaptered = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        parted = Project(
            base_folder=tmp_path,
            project_type=ProjectType.PARTED,
            parts=1,
        )

        assert standalone.is_standalone is True
        assert standalone.is_chaptered is False
        assert standalone.is_parted is False

        assert chaptered.is_standalone is False
        assert chaptered.is_chaptered is True
        assert chaptered.is_parted is False

        assert parted.is_standalone is False
        assert parted.is_chaptered is False
        assert parted.is_parted is True

    def test_save_creates_project_file(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            author="John Smith",
        )

        project.save()

        project_file = project.root / Project.FILE

        assert project_file.is_file()

    def test_save_stores_relative_paths(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
        )

        folder = project.root / "chapters"
        file = folder / "chapter-01.md"

        project.add_folder(folder)
        project.add_file(file, date(2026, 10, 4))

        project.save()

        project_file = project.root / Project.FILE

        data = json.loads(project_file.read_text(encoding="utf-8"))

        assert data["folders"] == [
            "chapters",
        ]

        assert data["files"] == {
            "chapters/chapter-01.md": "2026-10-04",
        }

    def test_save_and_load(self, tmp_path):
        original = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=3,
            author="John Smith",
            email="john@example.com",
            created_at=date(2026, 10, 1),
            updated_at=date(2026, 10, 3),
            folders=["notes", "chapters"],
            files={
                "master.md": date(2026, 10, 3),
                "chapter-01.md": date(2026, 10, 2),
            },
        )

        original.save()

        loaded = Project.load(original.root)

        assert loaded.base_folder == original.base_folder
        assert loaded.root == original.root
        assert loaded.title == original.title
        assert loaded.slug == original.slug
        assert loaded.project_type == original.project_type
        assert loaded.parts == original.parts
        assert loaded.locale == original.locale
        assert loaded.author == original.author
        assert loaded.email == original.email
        assert loaded.phone == original.phone
        assert loaded.created_at == original.created_at
        assert loaded.updated_at == original.updated_at
        assert loaded.folders == original.folders
        assert loaded.files == original.files

    def test_load_from_project_file(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
        )

        project.save()

        loaded = Project.load(project.root / Project.FILE)

        assert loaded.root == project.root
        assert loaded.title == project.title

    def test_load_from_child_folder(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
        )

        project.save()

        child = project.root / "chapters" / "part-01"
        child.mkdir(parents=True)

        loaded = Project.load(child)

        assert loaded.root == project.root

    def test_load_non_project_file_raises(self, tmp_path):
        file = tmp_path / "test.txt"
        file.write_text(
            "test",
            encoding="utf-8",
        )

        with pytest.raises(ValidationError):
            Project.load(file)

    def test_load_directory_without_project_raises(self, tmp_path):
        folder = tmp_path / "empty"
        folder.mkdir()

        with pytest.raises(ValidationError):
            Project.load(folder)
