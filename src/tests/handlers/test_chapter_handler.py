from datetime import date
from pathlib import Path

import pytest

from enums.project_type import ProjectType
from handlers.chapter_handler import ChapterHandler
from models.chapter import Chapter
from models.project import Project


class TestChapterHandler:

    @pytest.mark.parametrize(
        "project_type, parts, part, folder_name, file_name",
        [
            (
                ProjectType.STANDALONE,
                0,
                0,
                "texto",
                "v001_primeiro-capitulo.md",
            ),
            (
                ProjectType.CHAPTERED,
                0,
                0,
                "capitulos",
                "i0010_v001_primeiro-capitulo.md",
            ),
            (
                ProjectType.PARTED,
                1,
                1,
                "parte_01",
                "p001_i0010_v001_primeiro-capitulo.md",
            ),
        ],
    )
    def test_create(
        self,
        tmp_path: Path,
        project_type: ProjectType,
        parts: int,
        part: int,
        folder_name: str,
        file_name: str,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=project_type,
            parts=parts,
        )

        folder = project.root / folder_name
        folder.mkdir(parents=True)

        handler = ChapterHandler(project)

        file = handler.create(
            title="Primeiro capítulo",
            part=part,
        )

        assert file == folder / file_name
        assert file.exists()
        assert file.read_text(encoding="utf-8").startswith("# Primeiro capítulo\n")

        assert project.files[file] == date.today()

    def test_create_next_index(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        (folder / "i0010_v001_primeiro.md").touch()

        handler = ChapterHandler(project)

        file = handler.create("Segundo")

        assert file.name == ("i0020_v001_segundo.md")

    def test_create_version(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        source = folder / "i0010_v001_primeiro-capitulo.md"
        source.write_text(
            "# Primeiro capítulo\n\nConteúdo.\n",
            encoding="utf-8",
        )

        handler = ChapterHandler(project)

        file = handler.create_version(source)

        assert file == (folder / "i0010_v002_primeiro-capitulo.md")
        assert file.exists()

        assert file.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")

        assert project.files[file] == date.today()

    def test_create_version_with_new_title(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        source = folder / "i0010_v001_primeiro-capitulo.md"
        source.write_text(
            "# Primeiro capítulo\n\nConteúdo.\n",
            encoding="utf-8",
        )

        handler = ChapterHandler(project)

        file = handler.create_version(
            source,
            title="Novo título",
        )

        assert file == (folder / "i0010_v002_novo-titulo.md")

        assert file.read_text(encoding="utf-8") == "# Novo título\n\nConteúdo.\n"

    def test_copy_file(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "source.md"
        destination = tmp_path / "destination.md"

        source.write_text(
            "# Título\n\nConteúdo.\n",
            encoding="utf-8",
        )

        project = Project(
            base_folder=tmp_path,
        )
        handler = ChapterHandler(project)

        handler._copy_file(
            source_file=source,
            destination_file=destination,
            title=None,
        )

        assert destination.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")

    def test_copy_file_with_new_title(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "source.md"
        destination = tmp_path / "destination.md"

        source.write_text(
            "# Título antigo\n\nConteúdo.\n",
            encoding="utf-8",
        )

        project = Project(
            base_folder=tmp_path,
        )
        handler = ChapterHandler(project)

        handler._copy_file(
            source_file=source,
            destination_file=destination,
            title="Novo título",
        )

        assert destination.read_text(encoding="utf-8") == "# Novo título\n\nConteúdo.\n"

    def test_source_file_name(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        file = folder / "i0010_v001_primeiro-capitulo.md"
        file.touch()

        (folder / "i0010_v003_primeiro-capitulo.md").touch()

        chapter = Chapter(
            context=folder.name,
            part=0,
            index=10,
            version=1,
            slug="primeiro-capitulo",
        )

        handler = ChapterHandler(project)

        result = handler._source_file_name(
            chapter=chapter,
            file=file,
        )

        assert result == (folder / "i0010_v003_primeiro-capitulo.md")

    def test_destination_file_name(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        file = folder / "i0010_v003_primeiro-capitulo.md"
        file.touch()

        chapter = Chapter(
            context=folder.name,
            part=0,
            index=10,
            version=3,
            slug="primeiro-capitulo",
        )

        handler = ChapterHandler(project)

        result = handler._destination_file_name(
            chapter=chapter,
            title=None,
            file=file,
        )

        assert result == (folder / "i0010_v004_primeiro-capitulo.md")

    def test_destination_file_name_with_new_title(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        file = folder / "i0010_v003_primeiro-capitulo.md"
        file.touch()

        chapter = Chapter(
            context=folder.name,
            part=0,
            index=10,
            version=3,
            slug="primeiro-capitulo",
        )

        handler = ChapterHandler(project)

        result = handler._destination_file_name(
            chapter=chapter,
            title="Título alterado",
            file=file,
        )

        assert result == (folder / "i0010_v004_titulo-alterado.md")

    def test_create_content(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
        )
        handler = ChapterHandler(project)

        content = handler._create_content("  Primeiro capítulo  ")

        assert content == "# Primeiro capítulo"
