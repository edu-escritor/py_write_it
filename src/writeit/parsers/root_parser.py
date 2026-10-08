from pathlib import Path

from writeit.models.project import Project


class RootParser:

    @staticmethod
    def parse(path: str | Path) -> Path:
        path = Path(path).expanduser().resolve()

        if not path.exists():
            raise FileNotFoundError(f"'{path}' does not exist!")

        if path.is_file():
            path = path.parent

        for folder in (path, *path.parents):
            if (folder / Project.FILE).is_file():
                return folder

        raise FileNotFoundError(f"Could not find '{Project.FILE}' in '{path}' or its parents!")
