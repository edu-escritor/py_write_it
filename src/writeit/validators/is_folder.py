from pathlib import Path

from writeit.errors.validation_error import ValidationError


class IsFolder:

    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError("The value cannot be None!")

        if isinstance(value, str):
            return IsFolder._validate_string(value)

        return IsFolder._validate_path(value)

    @staticmethod
    def _validate_string(value: str) -> Path:
        value = value.strip()

        if not value:
            raise ValidationError("The value cannot be empty!")

        return IsFolder._validate_path(Path(value))

    @staticmethod
    def _validate_path(value: Path) -> Path:
        if not value.exists():
            raise ValidationError("The path does not exist!")

        if not value.is_dir():
            raise ValidationError("The path is not a directory!")

        return value.expanduser().resolve()
