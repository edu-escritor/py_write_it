import re
from pathlib import Path

from writeit.errors.validation_error import ValidationError
from writeit.validators.is_file import IsFile


class IsValidFile:
    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError(f"'{value}' does not exist!")

        file = IsFile.validate(value)

        if file.suffix != ".md":
            raise ValidationError(f"'{value}' does not have the correct extension!")

        pattern = r"(?:(?:p\d+_)?i\d+_)?v\d+_[a-z0-9]+(?:-[a-z0-9]+)*\.md"

        if not re.fullmatch(pattern, file.name):
            raise ValidationError("f'{value}' is invalid!")

        return file
