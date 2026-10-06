from typing import Annotated, Final

import typer

WRITE_IT_LABEL: Final[str] = "WritΞIt"

app = typer.Typer(
    name="writeit",
    help=f"[green]{WRITE_IT_LABEL}[/green]: " "manage your [green]writing[/green] like a [green]pro[/green].",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

project_app = typer.Typer(
    help="Manage your [green]project[/green].",
    no_args_is_help=True,
)

app.add_typer(
    project_app,
    name="project",
)


@project_app.command()
def create(
    title: Annotated[
        str,
        typer.Argument(
            help="Project title.",
        ),
    ],
) -> None:
    print(title)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
