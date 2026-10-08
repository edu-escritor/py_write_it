from pathlib import Path

import typer

from writeit.enums.image_type import ImageType
from writeit.handlers.image.image_handler import ImageHandler


def convert(
    source: Path = typer.Argument(..., help="Source image."),
    to: str = typer.Option(
        "jpg",
        "--to",
        "-t",
        help="Destination image format (jpg, png, webp, gif, ico, avif).",
    ),
) -> None:
    try:
        image_type = ImageType(f".{to.lower().lstrip('.')}")
    except ValueError:
        raise typer.BadParameter(f"Invalid image format: {to}")

    destination = ImageHandler.convert(source, image_type)

    typer.secho(
        f"Image converted: {destination}",
        fg=typer.colors.BRIGHT_BLUE,
    )
