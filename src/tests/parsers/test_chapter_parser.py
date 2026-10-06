from pathlib import Path

import pytest

from writeit.parsers.chapter_parser import ChapterParser
from writeit.models.chapter import Chapter


class TestChapterParser:

    @pytest.mark.parametrize(
        "file_name, context, part, index, version, slug",
        [
            (
                "v003_dedicatoria.md",
                "text",
                0,
                0,
                3,
                "dedicatoria",
            ),
            (
                "i0020_v003_dedicatoria-final.md",
                "chapters",
                0,
                20,
                3,
                "dedicatoria-final",
            ),
            (
                "p001_i0020_v003_dedicatoria.md",
                "parte-01",
                1,
                20,
                3,
                "dedicatoria",
            ),
        ],
    )
    def test_parse(
        self,
        tmp_path: Path,
        file_name: str,
        context: str,
        part: int | None,
        index: int | None,
        version: int,
        slug: str,
    ) -> None:
        folder = tmp_path / context
        folder.mkdir()

        file = folder / file_name
        file.touch()

        chapter = ChapterParser.parse(file)

        assert isinstance(chapter, Chapter)
        assert chapter.context == context
        assert chapter.part == part
        assert chapter.index == index
        assert chapter.version == version
        assert chapter.slug == slug
