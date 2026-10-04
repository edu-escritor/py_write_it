from errors.validation_error import ValidationError


class IsNotEmptyValidator:

    @staticmethod
    def validate(value: str | None) -> str:
        if value is None:
            raise ValidationError("The value cannot be empty!")

        value = value.strip()
        if not value:
            raise ValidationError("The value cannot be empty!")
        return value
