from enums.project_type import ProjectType
from handlers.project.project_create_handler import ProjectCreateHandler
from models.project import Project


class TestProjectCreateHandler:

    def test_create_standalone_project(self, tmp_path):
        handler = ProjectCreateHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        assert project.title == "The Last Horse"
        assert project.author == "John Smith"
        assert project.is_standalone
        assert (project.root / Project.FILE).is_file()

    def test_create_meta_folder(self, tmp_path):
        handler = ProjectCreateHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        folder = project.root / handler.FOLDER_META

        assert folder.is_dir()
        assert folder in project.folders
        assert (folder / handler.FILE_GITKEEP).is_file()

    def test_create_prompts_folder(self, tmp_path):
        handler = ProjectCreateHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        folder = project.root / handler.FOLDER_PROMPTS

        assert folder.is_dir()
        assert folder in project.folders
        assert (folder / handler.FILE_GITKEEP).is_file()

    def test_create_standalone_text_folder(self, tmp_path):
        handler = ProjectCreateHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
        )

        expected = project.root / handler._translate("files.segments.text")

        assert expected.is_dir()
        assert expected in project.folders

    def test_create_chaptered_project(self, tmp_path):
        handler = ProjectCreateHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.CHAPTERED,
        )

        expected = project.root / handler._translate("files.segments.chapters")

        assert expected.is_dir()
        assert expected in project.folders

    def test_create_parted_project(self, tmp_path):
        handler = ProjectCreateHandler(tmp_path)

        project = handler.create(
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.PARTED,
            parts=3,
        )

        name = handler._translate("files.segments.part")

        expected = [
            project.root / f"{name}_01",
            project.root / f"{name}_02",
            project.root / f"{name}_03",
        ]

        for folder in expected:
            assert folder.is_dir()
            assert folder in project.folders
            assert (folder / handler.FILE_GITKEEP).is_file()
