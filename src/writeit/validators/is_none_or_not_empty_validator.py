from writeit.errors.validation_error import ValidationError


class IsNoneOrNotEmptyValidator:

    @staticmethod
    def validate(value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValidationError("The value cannot be empty!")

        return value
