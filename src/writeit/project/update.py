from pathlib import Path
from typing import Annotated

import typer

from writeit.handlers.project.project_update_handler import ProjectUpdateHandler
from writeit.enums.project_field import ProjectField


def update(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Project folder.",
        ),
    ],
    author: Annotated[
        str | None,
        typer.Option(
            "--author",
            help="Project author.",
        ),
    ] = None,
    email: Annotated[
        str | None,
        typer.Option(
            "--email",
            help="Author email.",
        ),
    ] = None,
    phone: Annotated[
        str | None,
        typer.Option(
            "--phone",
            help="Author phone.",
        ),
    ] = None,
) -> None:
    handler = ProjectUpdateHandler(base_folder)

    fields = {
        ProjectField.AUTHOR: author,
        ProjectField.EMAIL: email,
        ProjectField.PHONE: phone,
    }

    for field, value in fields.items():
        if value is not None:
            handler.update(field, value)
            typer.secho(f"Project {field} update to {str(value)}", fg=typer.colors.BRIGHT_BLUE)
