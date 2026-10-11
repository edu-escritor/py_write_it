from pathlib import Path

from writeit.errors.validation_error import ValidationError


class HasContextFolder:

    @staticmethod
    def validate(value: str | Path) -> Path:
        path = Path(value)

        if path.parent == Path("."):
            raise ValidationError(f"The path '{path}' must include a parent folder!")

        return path
