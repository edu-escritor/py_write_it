from abc import ABC
from pathlib import Path
from typing import Final
from models.project import Project
from translations.translation_factory import TranslationFactory


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
