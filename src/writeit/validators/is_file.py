from pathlib import Path

from writeit.errors.validation_error import ValidationError


class IsFile:

    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError("The value cannot be None!")

        if isinstance(value, str):
            return IsFile._validate_string(value)

        return IsFile._validate_path(value)

    @staticmethod
    def _validate_string(value: str) -> Path:
        value = value.strip()

        if not value:
            raise ValidationError("The value cannot be empty!")

        return IsFile._validate_path(Path(value))

    @staticmethod
    def _validate_path(value: Path) -> Path:
        if not value.exists():
            raise ValidationError(f"'{value}' does not exist!")

        if not value.is_file():
            raise ValidationError(f"'{value}' is not a file!")

        return value.expanduser().resolve()
