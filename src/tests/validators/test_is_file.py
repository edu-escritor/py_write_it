# tests/test_is_file.py

import pytest

from writeit.validators.is_file import IsFile
from writeit.errors.validation_error import ValidationError


class TestIsFile:

    def test_accepts_existing_file(self, tmp_path):
        file = tmp_path / "file.txt"
        file.write_text("test")

        assert IsFile.validate(file) == file

    def test_accepts_existing_file_as_string(self, tmp_path):
        file = tmp_path / "file.txt"
        file.write_text("test")

        assert IsFile.validate(str(file)) == file

    def test_rejects_none(self):
        with pytest.raises(ValidationError):
            IsFile.validate(None)

    def test_rejects_empty_string(self):
        with pytest.raises(ValidationError):
            IsFile.validate("   ")

    def test_rejects_nonexistent_path(self, tmp_path):
        file = tmp_path / "does-not-exist.txt"

        with pytest.raises(ValidationError):
            IsFile.validate(file)

    def test_rejects_directory(self, tmp_path):
        with pytest.raises(ValidationError):
            IsFile.validate(tmp_path)
