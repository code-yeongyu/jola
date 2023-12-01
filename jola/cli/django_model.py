from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.theme import Theme
from typer import Exit

from jola.cli.typer_cli_application import LinterCLIApplication
from jola.linter.untyped_relationship_field import (
    fix_or_analyze_untyped_model,
)
from jola.models.relationship_field import (
    RelationshipField,
    RelationshipFieldsInFile,
)


class DjangoModelLinterCLI(LinterCLIApplication):
    def _print_warning_untyped_model(self, path: Path, relationship_fields: list[RelationshipField]) -> None:
        if not relationship_fields:
            return
        normal_console = Console(theme=Theme(inherit=False))
        texts = ""

        for relationship_field in relationship_fields:
            text = (
                f"[red bold]UNTYPED MODEL[/red bold] "
                f"[red]{path}[/red]:{relationship_field.start_line_number} "
                f"- Django Model Field [bold]{relationship_field.class_name}[/bold] "
                f"-> [bold underline]{relationship_field.field_name}[/bold underline] "
                f"is untyped [bold]{relationship_field.field_type}[/bold]"
            )
            if relationship_field.typed_code:
                text += " [italic][FIXABLE][/italic] "

            texts += text + "\n"

        normal_console.print(texts.strip())

    def _process_file(self, file_path: Path, fix: bool) -> Optional[RelationshipFieldsInFile]:
        try:
            result = fix_or_analyze_untyped_model(file_path, fix=fix)
            self._print_warning_untyped_model(result.path, result.relationship_fields)
            return result
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")
            return None

    def _process_files(self, file_paths: list[Path], fix: bool) -> list[Optional[RelationshipFieldsInFile]]:
        with Pool() as pool:
            process_partial = partial(self._process_file, fix=fix)
            return pool.map(process_partial, file_paths)

    def run(self, multi_process: bool, *args, **kwargs) -> None:
        results = []
        if multi_process:
            results = self._process_files(self.file_paths, self.fix)
        else:
            for file_path in self.file_paths:
                result = self._process_file(file_path, self.fix)
                if result:
                    results.append(result)

        if any(results):
            raise Exit(code=1)
