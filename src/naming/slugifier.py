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

        to_handle = Slugifier._apply_rules(text)
        to_handle = " ".join(to_handle.split()).strip()

        result = slugify(
            text=to_handle,
            separator=separator,
            lowercase=lowercase,
            max_length=max_length,
        )

        if not lowercase:
            result = result.upper()

        return result

    @staticmethod
    def _apply_rules(to_handle: str) -> str:
        to_handle = RemovePunctuationMarks().apply(to_handle)

        return RemoveStopWords().apply(to_handle)
