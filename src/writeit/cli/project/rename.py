from pathlib import Path
from typing import Annotated

import typer

from writeit.handlers.project.project_rename_handler import ProjectRenameHandler


def rename(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Project folder.",
        ),
    ],
    title: Annotated[
        str,
        typer.Option(
            "--title",
            help="New project title.",
        ),
    ],
) -> None:
    project = ProjectRenameHandler(base_folder).rename(title)
    typer.secho(f"Project renamed to:\n{str(project.root)}", fg=typer.colors.BRIGHT_BLUE)
