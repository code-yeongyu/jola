from enum import Enum
from pathlib import Path

from typer import Argument, Option, Typer

from jola.cli.django_model import DjangoModelLinterCLI

cli_app = Typer()


class LinterOptions(str, Enum):
    DJANGO_MODEL = "django-model"


linter_cli_dictionary = {
    LinterOptions.DJANGO_MODEL: DjangoModelLinterCLI,
}


@cli_app.command()
def jola(
    file_paths: list[Path] = Argument(
        ...,
        help="Paths to the files you want to analyze",
        exists=True,
        writable=True,
        resolve_path=True,
        allow_dash=True,
    ),
    rules: list[LinterOptions] = Option(
        [],
        "--rule",
        "-r",
        help="Specify the rule you want to run",
        case_sensitive=False,
    ),
    fix: bool = Option(
        False,
        "--fix",
        "-f",
        help="Fix the untyped models",
    ),
    multi_process: bool = Option(
        False,
        "--multi-process",
        "-m",
        help="Run the linter in multiple processes",
    ),
):
    options_to_run = [linter_cli_dictionary[option](file_paths=file_paths, fix=fix) for option in rules]

    for option in options_to_run:
        option.run(multi_process=multi_process)
