import shutil
import subprocess
import tempfile
from datetime import date
from importlib.resources import as_file, files
from pathlib import Path
from typing import Final

from writeit.compilers.base_compiler import BaseCompiler
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

    TEMPLATE_STANDALONE: Final[str] = "standalone.odt"
    TEMPLATE_CHAPTERED: Final[str] = "chaptered.odt"
    TEMPLATE_PARTED: Final[str] = "parted.odt"

    def __init__(self, project: Project) -> None:
        self._project: Project = project

    def assemble(self) -> Path:
        """Assemble the project content into a single master Markdown file."""
        if self._project.is_standalone:
            return StandaloneCompiler(self._project).compile()

        if self._project.is_chaptered:
            return ChapteredCompiler(self._project).compile()

        if self._project.is_parted:
            return PartedCompiler(self._project).compile()

        raise RuntimeError(f"Unsupported project type: {self._project.project_type}")

    def compile(self) -> Path:
        """Compile the master Markdown file into an ODT document."""
        source = self._project.root / BaseCompiler.FILE
        destination = self._project.root / (self._project.slug + "_" + date.today().isoformat() + ".odt")
        template = self._prepare_template()

        try:
            subprocess.run(
                [
                    self.PANDOC,
                    str(source),
                    "--from=" + "".join(self.OPTIONS),
                    "--reference-doc=" + str(template),
                    "--output=" + str(destination),
                ],
                check=True,
            )
        finally:
            template.unlink(missing_ok=True)

        return destination

    def build(self) -> Path:
        """Assemble the project and compile it into an ODT document."""
        self.assemble()

        return self.compile()

    def _prepare_template(self) -> Path:
        if self._project.is_chaptered:
            template = self.TEMPLATE_CHAPTERED
        elif self._project.is_parted:
            template = self.TEMPLATE_PARTED
        else:
            template = self.TEMPLATE_STANDALONE

        resource = files("writeit.resources").joinpath(template)

        with tempfile.NamedTemporaryFile(
            suffix=".odt",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)

        with as_file(resource) as source:
            shutil.copy(source, temporary_path)

        return temporary_path
