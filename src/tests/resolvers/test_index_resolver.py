from pathlib import Path

from enums.project_type import ProjectType
from models.project import Project
from resolvers.index_resolver import IndexResolver


class TestIndexResolver:

    def test_resolve_empty_folder(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        resolver = IndexResolver(project)

        assert resolver.resolve(folder) == 0

    def test_resolve_max_index(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        (folder / "i0010_v001_one.md").touch()
        (folder / "i0030_v001_two.md").touch()
        (folder / "i0020_v001_three.md").touch()

        resolver = IndexResolver(project)

        assert resolver.resolve(folder) == 30

    def test_next_index(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        (folder / "i0010_v001_one.md").touch()
        (folder / "i0020_v001_two.md").touch()

        resolver = IndexResolver(project)

        assert resolver.next(folder) == 30

    def test_next_rounds_to_ten(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        (folder / "i0027_v001_one.md").touch()

        resolver = IndexResolver(project)

        assert resolver.next(folder) == 30

    def test_standalone(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.STANDALONE,
        )

        resolver = IndexResolver(project)

        assert resolver.resolve(project.root) == 0
        assert resolver.next(project.root) == 0
