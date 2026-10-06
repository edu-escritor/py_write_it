from handlers.project.base_project_handler import BaseProjectHandler


class TestBaseProjectHandler:

    def test_load_project(self, tmp_path):
        from handlers.project.project_create_handler import ProjectCreateHandler

        creator = ProjectCreateHandler(tmp_path)

        original = creator.create(
            title="The Last Horse",
            author="John Smith",
        )

        loaded = BaseProjectHandler(original.root).load()

        assert loaded.root == original.root
        assert loaded.title == original.title
        assert loaded.author == original.author
