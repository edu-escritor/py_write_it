from typing import Final

class RemovePunctuationMarks:
    PUNCTUATION: Final[set[str]] = {
        ".", ",", ";", ":", "!", "?",
        "'", '"', "‘", "’", "“", "”",
        "…", "/", "\\",
    }

    def apply(self, text: str) -> str:
        applied = text
        for punctuation in self.PUNCTUATION:
            applied = applied.replace(punctuation, " ")

        return " ".join(applied.split()).strip()