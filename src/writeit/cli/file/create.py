from pathlib import Path
from typing import Annotated

import typer

from writeit.handlers.chapter_handler import ChapterHandler
from writeit.models.project import Project


def create(
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
            help="File title.",
        ),
    ],
    part: Annotated[
        int,
        typer.Option(
            "--part",
            help="Project part.",
        ),
    ] = 0,
) -> None:
    project = Project.load(base_folder)

    file = ChapterHandler(project).create(
        title=title,
        part=part,
    )

    typer.secho(f"File created:\n{str(file)}", fg=typer.colors.BRIGHT_BLUE)
