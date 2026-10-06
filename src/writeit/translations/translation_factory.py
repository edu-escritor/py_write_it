from writeit.translations.base_translation import BaseTranslation
from writeit.translations.english_american import EnglishAmerican
from writeit.translations.portuguese_european import PortugueseEuropean
from writeit.enums.locales import Locales


class TranslationFactory:

    @staticmethod
    def get(locale: Locales) -> type[BaseTranslation]:
        match locale:
            case Locales.PORTUGUESE_EUROPEAN:
                return PortugueseEuropean

            case Locales.ENGLISH_AMERICAN:
                return EnglishAmerican
