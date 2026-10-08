from pathlib import Path

import pytest

from writeit.errors.validation_error import ValidationError
from writeit.validators.is_valid_part_file import IsValidPartFile


class TestIsValidPartFile:

    @pytest.mark.parametrize(
        "file_name",
        [
            "p01_i0000_parte-01.md",
            "p1_i0000_parte-1.md",
            "p12_i0000_parte-12.md",
            "p123_i0000_parte-123.md",
        ],
    )
    def test_valid_file(
        self,
        tmp_path: Path,
        file_name: str,
    ) -> None:
        file = tmp_path / file_name
        file.touch()

        assert IsValidPartFile.validate(file) == file

    @pytest.mark.parametrize(
        "file_name",
        [
            "p01_i0010_parte-01.md",
            "p01_i0000_v01_parte-01.md",
            "i0000_parte-01.md",
            "p01_parte-01.md",
            "p01_i0000_parte.md",
            "p01_i0000_parte-.md",
            "p01_i0000_qualquer-01.md",
            "p01_i0000_parte-01.txt",
        ],
    )
    def test_invalid_file(
        self,
        tmp_path: Path,
        file_name: str,
    ) -> None:
        file = tmp_path / file_name
        file.touch()

        with pytest.raises(ValidationError):
            IsValidPartFile.validate(file)

    def test_none(self) -> None:
        with pytest.raises(ValidationError):
            IsValidPartFile.validate(None)

    def test_nonexistent_file(
        self,
        tmp_path: Path,
    ) -> None:
        file = tmp_path / "p01_i0000_parte-01.md"

        with pytest.raises(ValidationError):
            IsValidPartFile.validate(file)
