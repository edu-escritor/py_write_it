from typing import Final

import typer

from writeit.project import app as project_app

WRITE_IT_LABEL: Final[str] = "WritΞIt"

app = typer.Typer(
    name="writeit",
    help=(f"[green]{WRITE_IT_LABEL}[/green]: " "manage your [green]writing[/green] like a [green]pro[/green]."),
    no_args_is_help=True,
    rich_markup_mode="rich",
)

app.add_typer(
    project_app,
    name="project",
)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
