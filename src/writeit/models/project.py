import json
from datetime import date
from pathlib import Path
from typing import Final

from writeit.enums.locales import Locales
from writeit.enums.project_type import ProjectType
from writeit.errors.validation_error import ValidationError
from writeit.naming.slugifier import Slugifier
from writeit.validators.is_folder import IsFolder
from writeit.validators.is_none_or_not_empty_validator import IsNoneOrNotEmptyValidator
from writeit.validators.is_not_empty_validator import IsNotEmptyValidator
from writeit.validators.is_valida_project_part import IsValidProjectPart


class Project:
    FILE: Final[str] = ".writit_project"

    DEFAULT_TITLE: Final[str] = "Write It!"
    DEFAULT_AUTHOR: Final[str] = "John Doe"

    @classmethod
    def load(cls, path: Path) -> "Project":
        path = path.expanduser().resolve()

        if path.is_file():
            if path.name != cls.FILE:
                raise ValidationError(f"The file '{path}' is not a WritIt project file!")

            project_file = path

        elif path.is_dir():
            current = path

            while True:
                project_file = current / cls.FILE

                if project_file.is_file():
                    break

                if current == current.parent:
                    raise ValidationError("No WritIt project found!")

                current = current.parent

        else:
            raise FileNotFoundError(f"'{path}' does not exist!")

        data = json.loads(project_file.read_text(encoding="utf-8"))

        return cls(
            base_folder=project_file.parent.parent,
            title=data["title"],
            slug=data["slug"],
            project_type=ProjectType(data["project_type"]),
            parts=data["parts"],
            locale=Locales(data["locale"]),
            author=data["author"],
            email=data["email"],
            phone=data["phone"],
            created_at=date.fromisoformat(data["created_at"]),
            updated_at=(date.fromisoformat(data["updated_at"]) if data["updated_at"] is not None else None),
            folders=[Path(folder) for folder in data["folders"]],
            files={Path(file): date.fromisoformat(value) for file, value in data["files"].items()},
        )

    def __init__(
        self,
        base_folder: str | Path,
        title: str = DEFAULT_TITLE,
        slug: str | None = None,
        project_type: ProjectType = ProjectType.STANDALONE,
        parts: int = 0,
        locale: Locales = Locales.PORTUGUESE_EUROPEAN,
        author: str = DEFAULT_AUTHOR,
        email: str | None = None,
        phone: str | None = None,
        created_at: date | None = None,
        updated_at: date | None = None,
        folders: list[str | Path] | None = None,
        files: dict[str | Path, date] | None = None,
    ) -> None:
        self.base_folder = base_folder
        self.title = title
        self.slug = slug if slug is not None else Slugifier.slugify(title)
        self.project_type = project_type
        self.parts = parts
        self.locale = locale
        self.author = author
        self.email = email
        self.phone = phone
        self.created_at = date.today() if created_at is None else created_at
        self.updated_at = updated_at
        self.folders = [] if folders is None else folders
        self.files = {} if files is None else files

    @property
    def base_folder(self) -> Path:
        return self._base_folder

    @base_folder.setter
    def base_folder(self, value: str | Path) -> None:
        self._base_folder = IsFolder.validate(value)

    @property
    def root(self) -> Path:
        return self.base_folder / self.slug

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = IsNotEmptyValidator.validate(value)

    @property
    def slug(self) -> str:
        return self._slug

    @slug.setter
    def slug(self, value: str | None) -> None:
        if value is None:
            value = Slugifier.slugify(self.title)

        self._slug = IsNotEmptyValidator.validate(value)

    @property
    def project_type(self) -> ProjectType:
        return self._project_type

    @project_type.setter
    def project_type(self, value: ProjectType) -> None:
        self._project_type = value

    @property
    def parts(self) -> int:
        return self._parts

    @parts.setter
    def parts(self, value: int) -> None:
        self._parts = IsValidProjectPart.validate(
            value=value,
            project_type=self.project_type,
        )

    @property
    def locale(self) -> Locales:
        return self._locale

    @locale.setter
    def locale(self, value: Locales) -> None:
        self._locale = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        self._author = IsNotEmptyValidator.validate(value)

    @property
    def email(self) -> str | None:
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        self._email = IsNoneOrNotEmptyValidator.validate(value)

    @property
    def phone(self) -> str | None:
        return self._phone

    @phone.setter
    def phone(self, value: str | None) -> None:
        self._phone = IsNoneOrNotEmptyValidator.validate(value)

    @property
    def created_at(self) -> date:
        return self._created_at

    @created_at.setter
    def created_at(self, value: date) -> None:
        self._created_at = value

    @property
    def updated_at(self) -> date | None:
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: date | None) -> None:
        self._updated_at = value

    @property
    def folders(self) -> list[Path]:
        return [self.root / folder for folder in self._folders]

    @folders.setter
    def folders(
        self,
        value: list[str | Path],
    ) -> None:
        self._folders = sorted(self._relative_path(folder) for folder in value)

    def add_folder(
        self,
        folder: str | Path,
    ) -> None:
        folder = self._relative_path(folder)

        if folder in self._folders:
            return

        self._folders.append(folder)
        self._folders.sort()

    def remove_folder(
        self,
        folder: str | Path,
    ) -> None:
        folder = self._relative_path(folder)

        if folder not in self._folders:
            return

        self._folders.remove(folder)

    @property
    def files(self) -> dict[Path, date]:
        return {self.root / file: file_date for file, file_date in self._files.items()}

    @files.setter
    def files(
        self,
        value: dict[str | Path, date],
    ) -> None:
        self._files = dict(
            sorted(
                (
                    self._relative_path(file),
                    file_date,
                )
                for file, file_date in value.items()
            )
        )

    def add_file(
        self,
        file: str | Path,
        value: date,
    ) -> None:
        file = self._relative_path(file)

        if file in self._files:
            return

        self._files[file] = value
        self._files = dict(sorted(self._files.items()))

    def remove_file(
        self,
        file: str | Path,
    ) -> None:
        file = self._relative_path(file)

        if file not in self._files:
            return

        del self._files[file]

    @property
    def is_parted(self) -> bool:
        return self.project_type == ProjectType.PARTED

    @property
    def is_chaptered(self) -> bool:
        return self.project_type == ProjectType.CHAPTERED

    @property
    def is_standalone(self) -> bool:
        return self.project_type == ProjectType.STANDALONE

    def save(self) -> None:
        if self.created_at != date.today():
            self.updated_at = date.today()

        data = {
            "title": self.title,
            "slug": self.slug,
            "project_type": self.project_type.value,
            "parts": self.parts,
            "locale": self.locale.value,
            "author": self.author,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat(),
            "updated_at": (self.updated_at.isoformat() if self.updated_at is not None else None),
            "folders": [str(folder) for folder in self._folders],
            "files": {str(file): value.isoformat() for file, value in self._files.items()},
        }

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = self.root / self.FILE

        path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def contextualized_path(self, path: str | Path) -> str:
        path = Path(path)
        return str(path.relative_to(self.root))

    def _relative_path(
        self,
        value: str | Path,
    ) -> Path:
        path = Path(value)

        if path.is_absolute():
            try:
                return path.relative_to(self.root)
            except ValueError:
                raise ValidationError(f"The path '{path}' is outside the project!")

        return path
