from abc import ABC
from pathlib import Path

from writeit.translations.translation_factory import TranslationFactory
from writeit.models.project import Project


class BaseResolver(ABC):
    def __init__(self, project: Project | None = None) -> None:
        self._project: Project | None = project
        self._folder: Path | None = None

    @property
    def project(self) -> Project:
        if self._project is None:
            raise ValueError("Load the project first!")

        return self._project

    @property
    def folder(self) -> Path:
        if self._folder is None:
            raise ValueError("No folder given to resolver!")

        return self._folder

    @folder.setter
    def folder(self, folder: Path) -> None:
        folder = folder.expanduser().resolve()

        if not folder.exists():
            raise FileNotFoundError(f"The path '{folder}' does not exist!")

        if folder.is_file():
            folder = folder.parent

        root = self.project.root.resolve()

        if folder == root:
            raise ValueError("The folder cannot be the project root!")

        if not folder.is_relative_to(root):
            raise ValueError("The folder must be inside the project!")

        self._validate_folder(folder)

        self._folder = folder

    def _validate_folder(self, folder: Path) -> None:
        if self.project.is_standalone:
            parent = (self.project.root / self._translate("files.segments.text")).resolve()

            if not folder.is_relative_to(parent):
                raise ValueError("The folder must be inside the text folder!")

            return

        if self.project.is_chaptered:
            parent = (self.project.root / self._translate("files.segments.chapters")).resolve()

            if not folder.is_relative_to(parent):
                raise ValueError("The folder must be inside the chapters folder!")

            return

        if self.project.is_parted:
            relative = folder.relative_to(self.project.root.resolve())

            if not relative.parts:
                raise ValueError("The folder must be inside a part!")

            part_folder = relative.parts[0]
            part_name = self._translate("files.segments.part")

            if not part_folder.startswith(f"{part_name}_"):
                raise ValueError("The folder must be inside a part!")

    def _translate(self, key: str) -> str:
        translator = TranslationFactory.get(self.project.locale)

        return translator.translate(key)
