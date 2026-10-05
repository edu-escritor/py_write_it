import re
from pathlib import Path

from errors.validation_error import ValidationError
from validators.is_file import IsFile


class IsValidFile:
    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError("The path does not exist!")

        file = IsFile.validate(value)

        if file.suffix != ".md":
            raise ValidationError("The file does not have the correct extension!")

        pattern = r"(?:(?:p\d{3}_)?i\d{4}_)?" r"v\d{3}_" r"[a-z0-9]+(?:-[a-z0-9]+)*" r"\.md"

        if not re.fullmatch(pattern, file.name):
            raise ValidationError("The file is invalid!")

        return file
