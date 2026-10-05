from enums.locales import Locales
from translations.base_translation import BaseTranslation
from translations.english_american import EnglishAmerican
from translations.portuguese_european import PortugueseEuropean


class TranslationFactory:

    @staticmethod
    def get(locale: Locales) -> type[BaseTranslation]:
        match locale:
            case Locales.PORTUGUESE_EUROPEAN:
                return PortugueseEuropean

            case Locales.ENGLISH_AMERICAN:
                return EnglishAmerican
