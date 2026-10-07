import pytest

from writeit.enums.locales import Locales
from writeit.enums.project_type import ProjectType
from writeit.handlers.project.project_add_part_handler import ProjectAddPartHandler
from writeit.handlers.project.project_create_handler import ProjectCreateHandler
from writeit.helpers.segment_formatter import SegmentFormatter
from writeit.models.project import Project


class TestProjectAddPartHandler:

    def test_add_part(self, tmp_path):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.PARTED,
            parts=2,
        )

        handler = ProjectAddPartHandler(project.root)

        updated = handler.add_part()

        folder = project.root / SegmentFormatter.part_slug(value=3, locale=Locales.PORTUGUESE_EUROPEAN, connector="_")

        assert updated.parts == 3
        assert folder.is_dir()
        assert folder in updated.folders
        assert (folder / handler.FILE_GITKEEP).is_file()

        loaded = Project.load(project.root)

        assert loaded.parts == 3
        assert folder in loaded.folders

    def test_add_part_to_non_parted_project_raises(
        self,
        tmp_path,
    ):
        project = ProjectCreateHandler(tmp_path).create(
            title="The Last Horse",
            author="John Smith",
        )

        handler = ProjectAddPartHandler(project.root)

        with pytest.raises(
            RuntimeError,
            match="The project does not have parts!",
        ):
            handler.add_part()
