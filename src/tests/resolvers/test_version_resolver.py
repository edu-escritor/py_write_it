from pathlib import Path

from writeit.resolvers.version_resolver import VersionResolver
from writeit.enums.project_type import ProjectType
from writeit.models.project import Project


class TestVersionResolver:

    def test_resolve_max_version(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        file = folder / "i0020_v001_dedicatoria.md"
        file.touch()

        (folder / "i0020_v002_dedicatoria.md").touch()
        (folder / "i0020_v003_novo-titulo.md").touch()

        resolver = VersionResolver(project)

        assert resolver.resolve(file) == 3

    def test_next_version(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        file = folder / "i0020_v001_dedicatoria.md"
        file.touch()

        (folder / "i0020_v002_dedicatoria.md").touch()
        (folder / "i0020_v003_dedicatoria.md").touch()

        resolver = VersionResolver(project)

        assert resolver.next(file) == 4

    def test_ignores_other_chapters(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )
        folder = project.root / "capitulos"
        folder.mkdir(parents=True)

        file = folder / "i0020_v001_dedicatoria.md"
        file.touch()

        (folder / "i0020_v003_dedicatoria.md").touch()
        (folder / "i0030_v010_other.md").touch()

        resolver = VersionResolver(project)

        assert resolver.resolve(file) == 3

    def test_parted(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.PARTED,
            parts=1,
        )
        folder = project.root / "parte_01"
        folder.mkdir(parents=True)

        file = folder / "p001_i0020_v001_dedicatoria.md"
        file.touch()

        (folder / "p001_i0020_v005_novo-titulo.md").touch()

        resolver = VersionResolver(project)

        assert resolver.resolve(file) == 5
        assert resolver.next(file) == 6
