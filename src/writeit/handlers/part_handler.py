import re
from pathlib import Path
from typing import Final

from writeit.handlers.base_handler import BaseHandler
from writeit.models.project import Project


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

        file = self._create_file_name(part)
        content = self._create_content(part)
        file.write_text(content + "\n", "utf-8")

        return file

    def import_content(self, part: int) -> str:
        """Imports a new part file"""

        file = self._create_file_name(part)
        return self._read_file(file=file, is_part=True) + "\n\n"

    def _create_file_name(self, part: int) -> Path:
        part_index = f"{part:03}"

        part_slug = self._translate("files.segments.part")
        part_slug = f"{part_slug}-{part_index}"

        file = self.FILE_PATTERN.replace("«part_index»", part_index).replace("«part_slug»", part_slug)

        folder = self._get_part_folder(part)

        return folder / file

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
