from pathlib import Path
from typing import Annotated

import typer

from handlers.project.project_add_part_handler import ProjectAddPartHandler


def add_part(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Project folder.",
        ),
    ],
) -> None:
    project = ProjectAddPartHandler(base_folder).add_part()

    typer.secho(f"Project part added:\n{str(project.parts)}", fg=typer.colors.BRIGHT_BLUE)
