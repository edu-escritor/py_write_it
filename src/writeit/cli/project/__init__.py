import typer

from .add_part import add_part
from .create import create
from .rename import rename
from .update import update

app = typer.Typer(
    help="Manage your [green]project[/green].",
    no_args_is_help=True,
)

app.command()(create)
app.command()(rename)
app.command()(update)
app.command("add-part")(add_part)
