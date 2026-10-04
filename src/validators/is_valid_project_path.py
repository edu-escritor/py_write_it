from pathlib import Path

from errors.validation_error import ValidationError


class IsValidProjectPath:
    PROJECT_FILE = ".writit_project"

    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError("The value cannot be None!")

        path = Path(value)

        if path.exists():
            return IsValidProjectPath._validate_existing(path)

        return IsValidProjectPath._validate_new(path)

    @staticmethod
    def _validate_existing(path: Path) -> Path:
        if not path.is_dir():
            raise ValidationError("The path is not a directory!")

        project_file = path / IsValidProjectPath.PROJECT_FILE

        if not project_file.is_file():
            raise ValidationError("The directory is not a WritIt project!")

        return path

    @staticmethod
    def _validate_new(path: Path) -> Path:
        parent = path.parent

        if not parent.is_dir():
            raise ValidationError("The parent directory does not exist!")

        project_file = parent / IsValidProjectPath.PROJECT_FILE

        if project_file.exists():
            raise ValidationError("The parent directory is already a WritIt project!")

        return path
