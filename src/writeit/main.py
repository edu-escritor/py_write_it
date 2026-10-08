import sys
from typing import Final

import typer

from writeit.cli.compile import app as compile_app
from writeit.cli.file import app as file_app
from writeit.cli.image import app as image_app
from writeit.cli.project import app as project_app

WRITE_IT_LABEL: Final[str] = "WritΞIt"

app = typer.Typer(
    name="writeit",
    help=f"[green]{WRITE_IT_LABEL}[/green]: " "manage your [green]writing[/green] like a [green]pro[/green].",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

app.add_typer(
    project_app,
    name="project",
)

app.add_typer(
    file_app,
    name="file",
)

app.add_typer(
    compile_app,
    name="compile",
)

app.add_typer(
    image_app,
    name="image",
)


def main() -> None:
    debug = "--debug" in sys.argv or "-d" in sys.argv

    if debug:
        sys.argv = [arg for arg in sys.argv if arg not in ("--debug", "-d")]
        app()
        return

    try:
        app()
    except Exception as error:
        typer.secho(
            f"\n##### {WRITE_IT_LABEL} ΞRROR:\n {error}\n",
            fg=typer.colors.BRIGHT_RED,
            err=True,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
