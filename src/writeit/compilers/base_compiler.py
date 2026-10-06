from abc import ABC, abstractmethod
from datetime import date
from pathlib import Path
from typing import Final

from jinja2 import Environment, PackageLoader

from writeit.handlers.base_handler import BaseHandler
from writeit.models.project import Project
from writeit.parsers.chapter_parser import ChapterParser


class BaseCompiler(BaseHandler, ABC):
    TEMPLATE_MASTER: Final[str] = "create/master.md.j2"
    FILE: Final[str] = "master.md"

    def __init__(self, project: Project) -> None:
        super().__init__(project)
        self._content: str = ""

    def compile(self) -> Path:
        env = Environment(loader=PackageLoader("writeit", "views/templates"))
        template = env.get_template(self.TEMPLATE_MASTER)

        values = {
            "title": self.project.title,
            "author_label": self._translate("templates.master.author"),
            "author_name": self.project.author,
            "email_label": self._translate("templates.master.e-mail"),
            "author_email": self.project.email,
            "phone_label": self._translate("templates.master.phone"),
            "author_phone": self.project.phone,
            "date_label": self._translate("templates.master.date"),
            "date": date.today(),
            "words_label": self._translate("templates.master.words"),
            "words": self.count_words(),
            "characters_label": self._translate("templates.master.characters"),
            "characters": self.count_characters(),
        }

        master_content = template.render(**values).strip() + "\n\n" + self.content

        file = self.project.root / self.FILE
        file.write_text(
            data=master_content,
            encoding="utf-8",
        )

        return file

    @property
    def content(self) -> str:
        if self._content == "":
            self.update_content()

        return self._content

    @abstractmethod
    def update_content(self) -> None: ...

    def count_words(self) -> str:
        """Counts the number of words in the manuscript."""
        count = len(self.content.split())

        return f"{count:,}".replace(",", " ")

    def count_characters(
        self,
        without_spaces: bool = False,
    ) -> str:
        """Counts the number of characters in the manuscript."""
        content = self.content

        if without_spaces:
            content = "".join(content.split())

        count = len(content)

        return f"{count:,}".replace(",", " ")

    @staticmethod
    def find_chapters(folder: Path) -> list[Path]:
        files = [
            *folder.glob("i[0-9][0-9][0-9][0-9]_v[0-9][0-9][0-9]_*.md"),
            *folder.glob("p[0-9][0-9][0-9]_i[0-9][0-9][0-9][0-9]_v[0-9][0-9][0-9]_*.md"),
        ]

        return sorted(files)

    @staticmethod
    def find_latest_chapters(folder: Path) -> list[Path]:
        files = BaseCompiler.find_chapters(folder)
        result: list[Path] = []

        latest_identifier: str = ""
        latest_version: int = 0
        latest_file: Path | None = None

        for file in files:
            identifier, version = BaseCompiler._chapter_keys(file)

            if identifier != latest_identifier:
                if latest_file is not None:
                    result.append(latest_file)

                latest_identifier = identifier
                latest_version = version
                latest_file = file
                continue

            if version > latest_version:
                latest_version = version
                latest_file = file

        if latest_file is not None:
            result.append(latest_file)

        return result

    @staticmethod
    def _chapter_keys(file: Path) -> tuple[str, int]:
        chapter = ChapterParser.parse(file)
        identifier = f"{chapter.part}_{chapter.index}"

        return identifier, chapter.version
