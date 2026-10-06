import pytest

from writeit.resolvers.context_resolver import ContextResolver
from writeit.enums.project_type import ProjectType
from writeit.models.project import Project


class TestContextResolver:

    def test_resolve_standalone(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            author="John Smith",
        )

        resolver = ContextResolver(project)

        expected = project.root / resolver._translator.translate("files.segments.text")

        assert resolver.resolve() == expected

    def test_resolve_chaptered(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.CHAPTERED,
        )

        resolver = ContextResolver(project)

        expected = project.root / resolver._translator.translate("files.segments.chapters")

        assert resolver.resolve() == expected

    def test_resolve_parted(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.PARTED,
            parts=3,
        )

        resolver = ContextResolver(project)

        expected = project.root / f'{resolver._translator.translate("files.segments.part")}_02'

        assert resolver.resolve(2) == expected

    def test_resolve_parted_without_part_raises(self, tmp_path):
        project = Project(
            base_folder=tmp_path,
            title="The Last Horse",
            author="John Smith",
            project_type=ProjectType.PARTED,
            parts=3,
        )

        resolver = ContextResolver(project)

        with pytest.raises(
            ValueError,
            match="The part can't be None!",
        ):
            resolver.resolve()
