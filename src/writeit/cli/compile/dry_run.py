from pathlib import Path
from typing import Annotated

import typer

from writeit.compilers.master_compiler import MasterCompiler
from writeit.models.project import Project


def dry_run(
    base_folder: Annotated[
        Path,
        typer.Argument(
            help="Project folder.",
        ),
    ],
) -> None:
    project = Project.load(base_folder)
    tree = MasterCompiler(project).dry_run()
    print(tree)
