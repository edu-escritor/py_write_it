import typer

from .create import create
from .version import version

app = typer.Typer(
    help="Manage [green]files[/green].",
    no_args_is_help=True,
)

app.command(help="Create a new file.")(create)
app.command(help="Create a new version of a file.")(version)
