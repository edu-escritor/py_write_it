from typing import Final

import num2words

from writeit.enums.locales import Locales
from writeit.errors.validation_error import ValidationError
from writeit.translations.translation_factory import TranslationFactory


class SegmentFormatter:
    DIGITS_PART: Final[int] = 2
    DIGITS_INDEX: Final[int] = 4
    DIGITS_VERSION: Final[int] = 2

    @classmethod
    def part(cls, value: int | str) -> str:
        if int(value) == 0:
            return ""

        return f"p{cls.part_value(value)}"

    @classmethod
    def part_value(cls, value: int | str) -> str:
        return cls._format(value, cls.DIGITS_PART)

    @classmethod
    def part_slug(cls, value: int | str, locale: Locales, connector: str = "-") -> str:
        label = TranslationFactory.get(locale).translate("files.segments.part")

        return label + connector + cls.part_value(value)

    @classmethod
    def part_title(cls, value: int | str, locale: Locales) -> str:
        value = cls._validate(value, cls.DIGITS_PART)
        label = TranslationFactory.get(locale).translate("templates.part.title")
        word = num2words.num2words(number=value, lang=locale.value)

        return label.replace("«part»", word)

    @classmethod
    def index(cls, value: int | str, allow_zero: bool = False) -> str:
        if int(value) == 0 and not allow_zero:
            return ""

        return f"i{cls.index_value(value)}"

    @classmethod
    def index_value(cls, value: int | str) -> str:
        return cls._format(value, cls.DIGITS_INDEX)

    @classmethod
    def version(cls, value: int | str) -> str:
        if int(value) == 0:
            return ""

        return f"v{cls.version_value(value)}"

    @classmethod
    def version_value(cls, value: int | str) -> str:
        return cls._format(value, cls.DIGITS_VERSION)

    @classmethod
    def _format(cls, value: int | str, digits: int) -> str:
        value = cls._validate(value, digits)

        return f"{value:0{digits}d}"

    @classmethod
    def _validate(cls, value: int | str, digits: int) -> int:
        value = int(value)

        if value < 0:
            raise ValidationError(f"{value} is less than 0!")

        max_number = cls._max_number(digits)

        if value > max_number:
            raise ValidationError(f"{value} is more than {max_number}!")

        return value

    @classmethod
    def _max_number(cls, digits: int) -> int:
        return 10**digits - 1
