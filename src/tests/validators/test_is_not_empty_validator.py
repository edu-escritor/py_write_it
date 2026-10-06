import pytest

from writeit.validators.is_not_empty_validator import IsNotEmptyValidator
from writeit.errors.validation_error import ValidationError


class TestIsNotEmptyValidator:

    def test_returns_trimmed_value(self):
        assert IsNotEmptyValidator.validate("  hello  ") == "hello"

    def test_raises_error_when_value_is_none(self):
        with pytest.raises(ValidationError):
            IsNotEmptyValidator.validate(None)

    def test_raises_error_when_value_is_empty(self):
        with pytest.raises(ValidationError):
            IsNotEmptyValidator.validate("")

    def test_raises_error_when_value_has_only_whitespace(self):
        with pytest.raises(ValidationError):
            IsNotEmptyValidator.validate("   ")
