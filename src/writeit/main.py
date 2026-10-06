from typing import Final

import typer

from writeit.cli.compile import app as compile_app
from writeit.cli.file import app as file_app
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


def main() -> None:
    # try:
    app()
    # except Exception as error:
    #     typer.secho(
    #         f"\n##### {WRITE_IT_LABEL} ΞRROR: {error}\n",
    #         fg=typer.colors.BRIGHT_RED,
    #         err=True,
    #     )
    #     sys.exit(1)


if __name__ == "__main__":
    main()
