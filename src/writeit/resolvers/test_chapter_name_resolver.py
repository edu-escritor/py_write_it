from pathlib import Path

from writeit.resolvers.chapter_name_resolver import ChapterNameResolver
from writeit.enums.project_type import ProjectType
from writeit.models.project import Project


class TestChapterNameResolver:

    def test_standalone(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.STANDALONE,
        )

        resolver = ChapterNameResolver(project)

        result = resolver.resolve(
            title="Dedicatória",
            version=3,
        )

        assert result == "v003_dedicatoria.md"

    def test_chaptered(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.CHAPTERED,
        )

        resolver = ChapterNameResolver(project)

        result = resolver.resolve(
            title="Dedicatória",
            version=3,
            index=20,
        )

        assert result == "i0020_v003_dedicatoria.md"

    def test_parted(
        self,
        tmp_path: Path,
    ) -> None:
        project = Project(
            base_folder=tmp_path,
            project_type=ProjectType.PARTED,
            parts=2,
        )

        resolver = ChapterNameResolver(project)

        result = resolver.resolve(
            title="Dedicatória",
            version=3,
            index=20,
            part=2,
        )

        assert result == ("p002_i0020_v003_dedicatoria.md")
