from writeit.helpers.segment_formatter import SegmentFormatter
from writeit.naming.slugifier import Slugifier
from writeit.resolvers.base_resolver import BaseResolver


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

        slug = slug or Slugifier.slugify(title)

        segments: list[str] = []

        if self.project.is_parted:
            segment = SegmentFormatter.part(part)
            if segment != "":
                segments.append(segment)

        if not self.project.is_standalone:
            segment = SegmentFormatter.index(index)
            if segment != "":
                segments.append(segment)

        segment = SegmentFormatter.version(version)
        if segment != "":
            segments.append(segment)

        segments.append(slug)

        return "_".join(segments) + ".md"
