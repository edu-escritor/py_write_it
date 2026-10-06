import typer

from .assemble import assemble
from .build import build
from .compile import compile
from .dry_run import dry_run

app = typer.Typer(
    help="Compile the [green]project[/green].",
    no_args_is_help=True,
)

app.command()(assemble)
app.command("dry-run")(dry_run)
app.command()(compile)
app.command()(build)
