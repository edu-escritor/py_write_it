from pathlib import Path


class Finder:

    @classmethod
    def find_all(
        cls,
        folder: Path,
        *patterns: str,
    ) -> list[Path]:
        if not patterns:
            patterns = ("*.md",)

        files = [file for pattern in patterns for file in folder.glob(pattern)]

        return sorted(files)
