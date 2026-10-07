import pytest

from writeit.enums.project_type import ProjectType
from writeit.handlers.part_handler import PartHandler
from writeit.models.project import Project
from writeit.resolvers.context_resolver import ContextResolver


class TestPartHandler:

    def test_standalone_project_raises(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.STANDALONE,
        )

        with pytest.raises(
            ValueError,
            match="The project does not have parts!",
        ):
            PartHandler(project)

    def test_chaptered_project_raises(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.CHAPTERED,
        )

        with pytest.raises(
            ValueError,
            match="The project does not have parts!",
        ):
            PartHandler(project)

    def test_create_file(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=1,
        )
        project.root.mkdir()

        handler = PartHandler(project)

        folder = ContextResolver(project).resolve(1)

        folder.mkdir()

        file = handler.create(1)

        assert file.is_file()
        assert file.parent == folder
        assert file.name == "p01_i0000_parte-01.md"

    def test_create_file_content(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=1,
        )
        project.root.mkdir()

        handler = PartHandler(project)

        folder = ContextResolver(project).resolve(1)
        folder.mkdir()

        file = handler.create(1)

        assert file.read_text(encoding="utf-8").startswith("# Parte 1\n")

    def test_create_file_name(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=12,
        )

        handler = PartHandler(project)

        file = handler.create_file_name(12)

        assert file == (ContextResolver(project).resolve(12) / "p12_i0000_parte-12.md")

    def test_create_file_name_pads_part_index(
        self,
        tmp_path,
    ):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=1,
        )

        handler = PartHandler(project)

        file = handler.create_file_name(1)

        assert file.name == "p01_i0000_parte-01.md"

    def test_import_content(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=1,
        )
        project.root.mkdir()

        handler = PartHandler(project)

        folder = ContextResolver(project).resolve(1)
        folder.mkdir()

        handler.create(1)

        content = handler.import_content(1)

        assert content.startswith("## Parte 1\n")

    def test_import_content_file_not_found(
        self,
        tmp_path,
    ):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            project_type=ProjectType.PARTED,
            parts=1,
        )

        handler = PartHandler(project)

        with pytest.raises(FileNotFoundError):
            handler.import_content(1)
