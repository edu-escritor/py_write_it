from pathlib import Path
from typing import Annotated

import typer

from writeit.handlers.normalize.file_normalize_handler import FileNormalizeHandler


def normalize(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Base folder.",
        ),
    ],
) -> None:
    files = FileNormalizeHandler(base_folder).normalize()
    if not files:
        typer.secho(f"No files needed to be normalized.", fg=typer.colors.BRIGHT_GREEN)
        return

    typer.secho(f"Normalized files:", fg=typer.colors.BRIGHT_BLUE)
    for file in files:
        typer.secho(f"    {file}", fg=typer.colors.BRIGHT_BLUE)
