from naming.slugifier import Slugifier
from resolvers.base_resolver import BaseResolver


class ChapterNameResolver(BaseResolver):

    def resolve(
        self,
        version: int,
        title: str | None = None,
        slug: str | None = None,
        index: int = 0,
        part: int = 0,
    ) -> str:
        if title is None and slug is None:
            raise ValueError("Title or slug is required!")

        if slug is None:
            slug = Slugifier.slugify(title)

        segments: list[str] = []

        if self.project.is_parted:
            segments.append(f"p{part:03}")

        if not self.project.is_standalone:
            segments.append(f"i{index:04}")

        segments.append(f"v{version:03}")
        segments.append(slug)

        return "_".join(segments) + ".md"
