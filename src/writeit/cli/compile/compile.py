from pathlib import Path
from typing import Annotated

import typer

from writeit.compilers.master_compiler import MasterCompiler
from writeit.models.project import Project


def compile(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Project folder.",
        ),
    ],
) -> None:
    project = Project.load(base_folder)
    file = MasterCompiler(project).compile()

    typer.secho(
        f"Project compiled:\n{file}",
        fg=typer.colors.BRIGHT_BLUE,
    )
