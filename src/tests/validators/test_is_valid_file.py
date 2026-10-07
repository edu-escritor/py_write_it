from pathlib import Path

import pytest

from writeit.errors.validation_error import ValidationError
from writeit.validators.is_valid_file import IsValidFile


class TestIsValidFile:

    @pytest.mark.parametrize(
        "file_name",
        [
            "v003_dedicatoria.md",
            "v003_dedicatoria-final.md",
            "i0020_v003_dedicatoria.md",
            "i0020_v003_dedicatoria-final.md",
            "p001_i0020_v003_dedicatoria.md",
            "p001_i0020_v003_dedicatoria-final.md",
        ],
    )
    def test_valid_file(
        self,
        tmp_path: Path,
        file_name: str,
    ) -> None:
        file = tmp_path / file_name
        file.touch()

        assert IsValidFile.validate(file) == file

    @pytest.mark.parametrize(
        "file_name",
        [
            "dedicatoria.md",
            "v_dedicatoria.md",
            "i0020_dedicatoria.md",
            "p01_i0020_dedicatoria.md",
            "p01_v03_dedicatoria.md",
            "v03_-dedicatoria.md",
            "v03_dedicatoria-.md",
            "v03_dedicatoria--final.md",
            "v03_dedicatoria.txt",
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
            IsValidFile.validate(file)

    def test_none(self) -> None:
        with pytest.raises(ValidationError):
            IsValidFile.validate(None)

    def test_file_does_not_exist(
        self,
        tmp_path: Path,
    ) -> None:
        file = tmp_path / "v001_chapter.md"

        with pytest.raises(ValidationError):
            IsValidFile.validate(file)
