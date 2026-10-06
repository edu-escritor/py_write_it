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
    ProjectAddPartHandler(base_folder).add_part()
