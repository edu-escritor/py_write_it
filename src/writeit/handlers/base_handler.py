from abc import ABC
from pathlib import Path
from typing import Final

from jinja2 import Environment, PackageLoader

from writeit.models.project import Project
from writeit.translations.translation_factory import TranslationFactory


class BaseHandler(ABC):
    FILE_GITKEEP: Final[str] = ".gitkeep"

    def __init__(self, project: Project | None = None) -> None:
        self._project: Project | None = project

    @property
    def project(self) -> Project:
        if self._project is None:
            raise ValueError("Load the project first!")

        return self._project

    def _translate(self, key: str) -> str:
        translator = TranslationFactory.get(self.project.locale)

        return translator.translate(key)

    def _create_folder(self, folder: Path) -> None:
        folder.mkdir(exist_ok=True)

        self._add_gitkeep(folder)
        self.project.add_folder(folder)
        self.project.save()

    def _add_gitkeep(self, folder: Path) -> None:
        file = folder / self.FILE_GITKEEP
        file.write_text("", encoding="utf-8")

    def render_template(self, template_name: str, values: dict[str, str]) -> str:
        env = Environment(loader=PackageLoader("writeit", "views/templates"))
        template = env.get_template(template_name)
        return template.render(**values)

    def _read_file(
        self,
        file: Path,
        is_part: bool = False,
    ) -> str:
        if not file.exists():
            raise FileNotFoundError(f"File not found: {file}")

        if is_part and not self.project.is_parted:
            raise ValueError("The project does not have parts!")

        content = file.read_text(encoding="utf-8")

        if is_part:
            level = "##"
        elif self.project.is_parted:
            level = "###"
        else:
            level = "##"

        lines = content.splitlines()

        if lines:
            lines[0] = (
                lines[0]
                .strip()
                .replace(
                    "# ",
                    f"{level} ",
                    1,
                )
            )

        return "\n".join(lines).strip()
