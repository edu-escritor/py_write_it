import typer

from .assemble import assemble
from .build import build
from .compile import compile
from .dry_run import dry_run

app = typer.Typer(
    help="Compile the [green]project[/green].",
    no_args_is_help=True,
)

app.command(help="Assemble the project into a single Markdown file.")(assemble)
app.command("dry-run", help="List the files that will be assembled into the single Markdown file.")(dry_run)
app.command(help="Compile the assembled Markdown into a LibreOffice document.")(compile)
app.command(help="Assemble and compile the project.")(build)
