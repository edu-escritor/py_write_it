import re
from pathlib import Path

from writeit.enums.locales import Locales
from writeit.errors.validation_error import ValidationError
from writeit.helpers.segment_formatter import SegmentFormatter
from writeit.translations.translation_factory import TranslationFactory
from writeit.validators.is_file import IsFile


class IsValidPartFile:

    @staticmethod
    def validate(value: str | Path | None) -> Path:
        if value is None:
            raise ValidationError(f"'{value}' does not exist!")

        file = IsFile.validate(value)

        if file.suffix != ".md":
            raise ValidationError(f"'{value}' does not have the correct extension!")

        index = SegmentFormatter.index(
            value=0,
            allow_zero=True,
        )

        for locale in Locales:
            translator = TranslationFactory.get(locale)
            label = translator.translate("files.segments.part")

            pattern = rf"p\d+_{index}_" rf"{re.escape(label)}-\d+\.md"

            if re.fullmatch(pattern, file.name):
                return file

        raise ValidationError(f"'{value}' is invalid!")
