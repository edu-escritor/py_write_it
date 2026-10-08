import typer

from .add_part import add_part
from .create import create
from .normalize import normalize
from .rename import rename
from .update import update

app = typer.Typer(
    help="Manage your [green]project[/green].",
    no_args_is_help=True,
)

app.command(help="Create a new project.")(create)
app.command(help="Rename the project.")(rename)
app.command(help="Update project metadata.")(update)
app.command("add-part", help="Add a new part to the project.")(add_part)
app.command(help="Normalize project file names.")(normalize)
