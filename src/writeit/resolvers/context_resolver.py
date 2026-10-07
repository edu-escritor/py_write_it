from pathlib import Path

from writeit.helpers.segment_formatter import SegmentFormatter
from writeit.models.project import Project
from writeit.resolvers.base_resolver import BaseResolver
from writeit.translations.base_translation import BaseTranslation
from writeit.translations.translation_factory import TranslationFactory


class ContextResolver(BaseResolver):

    def __init__(self, project: Project) -> None:
        super().__init__(project)
        self._translator: type[BaseTranslation] = TranslationFactory.get(self.project.locale)

    def resolve(self, part: int | None = None) -> Path:
        resolve = self._resolve_standalone()
        if resolve is None:
            resolve = self._resolve_chaptered()
        if resolve is None:
            resolve = self._resolve_part(part)
        if resolve is None:
            raise ValueError("The project has no context!")
        return resolve

    def _resolve_standalone(self) -> Path | None:
        if not self.project.is_standalone:
            return None

        return self.project.root / self._translator.translate("files.segments.text")

    def _resolve_chaptered(self) -> Path | None:
        if not self.project.is_chaptered:
            return None

        return self.project.root / self._translator.translate("files.segments.chapters")

    def _resolve_part(self, part: int | None = None) -> Path | None:
        if not self.project.is_parted:
            return None

        if part is None or part == 0:
            raise ValueError("The part can't be None!")

        return self.project.root / SegmentFormatter.part_slug(value=part, locale=self.project.locale, connector="_")
