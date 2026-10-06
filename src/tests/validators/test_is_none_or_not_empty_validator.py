import pytest

from writeit.validators.is_none_or_not_empty_validator import IsNoneOrNotEmptyValidator
from writeit.errors.validation_error import ValidationError


class TestIsNoneOrNotEmptyValidator:

    def test_returns_none_when_value_is_none(self):
        assert IsNoneOrNotEmptyValidator.validate(None) is None

    def test_returns_trimmed_value(self):
        assert IsNoneOrNotEmptyValidator.validate("  hello  ") == "hello"

    def test_raises_error_when_value_is_empty(self):
        with pytest.raises(ValidationError):
            IsNoneOrNotEmptyValidator.validate("")

    def test_raises_error_when_value_has_only_whitespace(self):
        with pytest.raises(ValidationError):
            IsNoneOrNotEmptyValidator.validate("   ")
