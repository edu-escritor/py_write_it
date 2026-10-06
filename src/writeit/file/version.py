from pathlib import Path
from typing import Annotated

import typer

from writeit.handlers.chapter_handler import ChapterHandler
from writeit.models.project import Project


def version(
    file: Annotated[
        Path,
        typer.Argument(
            help="File to version.",
        ),
    ],
    title: Annotated[
        str | None,
        typer.Option(
            "--title",
            help="New file title.",
        ),
    ] = None,
) -> None:
    project = Project.load(file.parent)

    file = ChapterHandler(project).create_version(
        file=file,
        title=title,
    )

    typer.secho(f"File version created:\n{str(file)}", fg=typer.colors.BRIGHT_BLUE)
