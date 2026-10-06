from pathlib import Path
from typing import Final

from writeit.compilers.chaptered_compiler import ChapteredCompiler
from writeit.compilers.parted_compiler import PartedCompiler
from writeit.compilers.standalone_compiler import StandaloneCompiler
from writeit.models.project import Project


class MasterCompiler:

    PANDOC: Final[str] = "/usr/bin/pandoc"
    OPTIONS: Final[tuple[str, ...]] = (
        "markdown",
        "-auto_identifiers",
        "-hard_line_breaks",
    )

    TEMPLATE_PARTED = "parted.odt"

    def __init__(self, project: Project) -> None:
        self._project: Project = project

    def assemble(self) -> Path:
        if self._project.is_standalone:
            return StandaloneCompiler(self._project).compile()

        if self._project.is_chaptered:
            return ChapteredCompiler(self._project).compile()

        if self._project.is_parted:
            return PartedCompiler(self._project).compile()

        raise RuntimeError(f"Unsupported project type: {self._project.project_type}")
