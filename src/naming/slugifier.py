from slugify import slugify

from naming.rules.remove_punctuation_marks import RemovePunctuationMarks
from naming.rules.remove_stop_words import RemoveStopWords


class Slugifier:
    @staticmethod
    def slugify(
        text: str,
        separator: str = "-",
        lowercase: bool = True,
        max_length: int = 250,
    ) -> str:

        result = Slugifier._apply_rules(text)
        result = " ".join(result.split()).strip()

        result = slugify(
            text=result,
            separator=" ",
            lowercase=lowercase,
            max_length=max_length,
        )

        result = Slugifier._apply_rules(result)
        result = " ".join(result.split()).strip()

        result = result.replace(" ", separator)

        if not lowercase:
            result = result.upper()

        return result

    @staticmethod
    def _apply_rules(to_handle: str) -> str:
        to_handle = RemovePunctuationMarks().apply(to_handle)

        return RemoveStopWords().apply(to_handle)
