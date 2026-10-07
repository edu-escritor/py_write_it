import re
from pathlib import Path
from typing import Final

from writeit.handlers.base_handler import BaseHandler
from writeit.helpers.segment_formatter import SegmentFormatter
from writeit.models.project import Project
from writeit.resolvers.context_resolver import ContextResolver


class PartHandler(BaseHandler):

    FILE_PATTERN: Final[str] = "p«part_index»_i0000_«part_slug».md"

    def __init__(self, project: Project) -> None:
        super().__init__(project)
        if not self.project.is_parted:
            raise ValueError("The project does not have parts!")

    @staticmethod
    def is_part_file(file: Path) -> bool:
        return re.search(r"(?:^|_)i0+(?:_|\.md$)", file.name) is not None

    def create(self, part: int) -> Path:
        """Creates a new part file"""

        file = self.create_file_name(part)
        content = self._create_content(part)
        file.write_text(content + "\n", "utf-8")

        return file

    def import_content(self, part: int) -> str:
        """Imports a new part file"""

        file = self.create_file_name(part)
        return self._read_file(file=file, is_part=True) + "\n\n"

    def create_file_name(self, part: int) -> Path:
        segments: list[str] = [
            SegmentFormatter.part(part),
            SegmentFormatter.index(value=0, allow_zero=True),
            SegmentFormatter.part_slug(
                value=part,
                locale=self.project.locale,
            ),
        ]

        return ContextResolver(self.project).resolve(part) / ("_".join(segments) + ".md")

    def _create_content(self, part: int) -> str:
        values: dict[str, str] = {
            "title": self._translate("templates.part.title").replace(
                "«part»",
                str(part),
            )
        }

        return self.render_template(
            "create/part.md.j2",
            values,
        ).strip()
