import typer

from writeit.cli.image.convert import convert

app = typer.Typer(
    help="Convert images.",
    no_args_is_help=True,
)

app.command(help="Convert an image to another format.")(convert)
