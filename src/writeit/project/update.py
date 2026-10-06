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
