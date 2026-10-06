import re
from pathlib import Path

from writeit.resolvers.base_resolver import BaseResolver


class IndexResolver(BaseResolver):

    def resolve(self, path: Path) -> int:
        if self.project.is_standalone:
            return 0

        self.folder = path

        return self._get_max_index()

    def next(self, path: Path) -> int:
        index = self.resolve(path)

        if self.project.is_standalone:
            return 0

        return ((index // 10) + 1) * 10

    def _get_max_index(self) -> int:
        indexes: list[int] = []

        for file in self.folder.glob("*.md"):
            match = re.search(
                r"(?:^|_)i(\d{4})(?:_|$)",
                file.stem,
            )

            if match:
                indexes.append(int(match.group(1)))

        return max(indexes, default=0)
