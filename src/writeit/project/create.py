from pathlib import Path
from typing import Annotated

import typer

from writeit.handlers.project.project_create_handler import ProjectCreateHandler
from writeit.enums.project_type import ProjectType
from writeit.enums.locales import Locales


def create(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Base folder.",
        ),
    ],
    title: Annotated[
        str,
        typer.Option(
            "--title",
            help="Project title.",
        ),
    ],
    author: Annotated[
        str,
        typer.Option(
            "--author",
            help="Project author.",
        ),
    ],
    project_type: Annotated[
        ProjectType,
        typer.Option(
            "--type",
            help="Project type.",
        ),
    ] = ProjectType.STANDALONE,
    parts: Annotated[
        int,
        typer.Option(
            "--parts",
            help="Number of parts.",
        ),
    ] = 0,
    locale: Annotated[
        Locales,
        typer.Option(
            "--locale",
            help="Project locale.",
        ),
    ] = Locales.PORTUGUESE_EUROPEAN,
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
    if parts >= 1:
        project_type = ProjectType.PARTED

    project = ProjectCreateHandler(base_folder).create(
        title=title,
        author=author,
        project_type=project_type,
        parts=parts,
        locale=locale,
        email=email,
        phone=phone,
    )

    typer.secho(f"Project created:\n{str(project.root)}", fg=typer.colors.BRIGHT_BLUE)
