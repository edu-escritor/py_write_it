class BaseTranslation:

    TRANSLATIONS: dict[str, str] = {}

    @classmethod
    def translate(cls, key: str) -> str:
        if key not in cls.TRANSLATIONS:
            raise ValueError(f"Key {key} is not a valid key!")

        return cls.TRANSLATIONS[key]
