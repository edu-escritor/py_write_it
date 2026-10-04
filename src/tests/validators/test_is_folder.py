# tests/test_is_folder.py

import pytest

from errors.validation_error import ValidationError
from validators.is_folder import IsFolder


class TestIsFolder:

    def test_accepts_existing_directory(self, tmp_path):
        assert IsFolder.validate(tmp_path) == tmp_path

    def test_accepts_existing_directory_as_string(self, tmp_path):
        assert IsFolder.validate(str(tmp_path)) == tmp_path

    def test_rejects_none(self):
        with pytest.raises(ValidationError):
            IsFolder.validate(None)

    def test_rejects_empty_string(self):
        with pytest.raises(ValidationError):
            IsFolder.validate("   ")

    def test_rejects_nonexistent_path(self, tmp_path):
        path = tmp_path / "does-not-exist"

        with pytest.raises(ValidationError):
            IsFolder.validate(path)

    def test_rejects_file(self, tmp_path):
        file = tmp_path / "file.txt"
        file.write_text("test")

        with pytest.raises(ValidationError):
            IsFolder.validate(file)
