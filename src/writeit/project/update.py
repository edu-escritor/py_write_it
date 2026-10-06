from pathlib import Path
from typing import Annotated

import typer

from enums.project_field import ProjectField
from handlers.project.project_update_handler import ProjectUpdateHandler


def update(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Project folder.",
        ),
    ],
    field: Annotated[
        ProjectField,
        typer.Option(
            "--field",
            help="Project field.",
        ),
    ],
    value: Annotated[
        str,
        typer.Option(
            "--value",
            help="New value.",
        ),
    ],
) -> None:
    ProjectUpdateHandler(base_folder).update(
        field,
        value,
    )
