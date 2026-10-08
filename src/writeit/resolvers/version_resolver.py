import re
from pathlib import Path

from writeit.helpers.finder import Finder
from writeit.resolvers.base_resolver import BaseResolver


class VersionResolver(BaseResolver):

    def resolve(self, path: Path) -> int:
        if not path.is_file():
            raise ValueError(f"'{path}' must be a file!")

        self.folder = path

        index = self._get_index(path)

        return self._get_max_version(index)

    def next(self, path: Path) -> int:
        return self.resolve(path) + 1

    def _get_index(
        self,
        file: Path,
    ) -> int | None:
        match = re.search(
            r"(?:^|_)i(\d+)(?:_|$)",
            file.stem,
        )

        if match is None:
            return None

        return int(match.group(1))

    def _get_max_version(
        self,
        index: int | None,
    ) -> int:
        versions: list[int] = []

        for file in Finder.find_all(self.folder):
            if self._get_index(file) != index:
                continue

            match = re.search(
                r"(?:^|_)v(\d+)(?:_|$)",
                file.stem,
            )

            if match:
                versions.append(int(match.group(1)))

        return max(versions, default=0)
