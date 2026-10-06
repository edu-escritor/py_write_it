from typing import Final

class RemoveStopWords:
    STOP_WORDS_EN: Final[set[str]] = {
        "a", "an", "the",
        "of", "in", "on", "at",
        "by", "for", "from",
        "with", "to",
        "and", "or",
        "that",
        "if",
    }

    STOP_WORDS_PT: Final[set[str]] = {
        "a", "as", "o", "os",
        "um", "uma", "uns", "umas",
        "de", "da", "das", "do", "dos",
        "em", "na", "nas", "no", "nos",
        "por", "pela", "pelas", "pelo", "pelos",
        "para",
        "com",
        "e", "ou",
        "que",
        "se",
    }

    def apply(self, text: str) -> str:
        applied: list[str] = []

        words = text.split()

        for word in words:
            if word.lower() in self.STOP_WORDS_EN or word.lower() in self.STOP_WORDS_PT:
                continue

            applied.append(word)

        return " ".join(applied).strip()