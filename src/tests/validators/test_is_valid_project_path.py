import pytest

from writeit.errors.validation_error import ValidationError
from writeit.validators.is_valid_project_path import IsValidProjectPath


class TestIsValidProjectPath:

    def test_accepts_existing_project(self, tmp_path):
        project = tmp_path / "my-project"
        project.mkdir()

        project_file = project / ".writit_project"
        project_file.write_text("{}")

        assert IsValidProjectPath.validate(project) == project

    def test_rejects_existing_directory_without_project_file(self, tmp_path):
        project = tmp_path / "my-project"
        project.mkdir()

        with pytest.raises(ValidationError):
            IsValidProjectPath.validate(project)

    def test_rejects_existing_file(self, tmp_path):
        file = tmp_path / "file.txt"
        file.write_text("test")

        with pytest.raises(ValidationError):
            IsValidProjectPath.validate(file)

    def test_accepts_new_project_path_when_parent_exists(self, tmp_path):
        project = tmp_path / "new-project"

        assert IsValidProjectPath.validate(project) == project

    def test_rejects_new_project_when_parent_does_not_exist(self, tmp_path):
        project = tmp_path / "missing-parent" / "new-project"

        with pytest.raises(ValidationError):
            IsValidProjectPath.validate(project)

    def test_rejects_new_project_inside_existing_project(self, tmp_path):
        project_file = tmp_path / ".writit_project"
        project_file.write_text("{}")

        new_project = tmp_path / "new-project"

        with pytest.raises(ValidationError):
            IsValidProjectPath.validate(new_project)

    def test_rejects_none(self):
        with pytest.raises(ValidationError):
            IsValidProjectPath.validate(None)
