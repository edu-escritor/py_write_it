from pathlib import Path

from writeit.enums.image_type import ImageType
from writeit.errors.validation_error import ValidationError
from writeit.validators.is_file import IsFile


class IsValidImage:
    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError(f"'{value}' does not exist!")

        file = IsFile.validate(value)

        try:
            ImageType(file.suffix.lower())
        except ValueError:
            raise ValidationError(f"'{file}' is not an image file!")

        return file
