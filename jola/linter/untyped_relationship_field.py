from pathlib import Path

from jola.analyzer import find_untyped_relationship_fields
from jola.fixer import fix_untyped_relationship_field
from jola.models.relationship_field import (
    RelationshipFieldsInFile,
)
from jola.utils import get_source_code


def fix_or_analyze_untyped_model(file_path: Path, fix: bool):
    source_code = get_source_code(file_path)
    untyped_relationship_fields = find_untyped_relationship_fields(source_code)

    try:
        file_path.relative_to(Path.cwd())
    except ValueError:
        pass

    if fix:
        fixed_source_code = fix_untyped_relationship_field(source_code, untyped_relationship_fields)
        with open(file_path, "w") as f:
            f.write(fixed_source_code)
        source_code = get_source_code(file_path)
        untyped_relationship_fields = find_untyped_relationship_fields(source_code)

    return RelationshipFieldsInFile(
        path=file_path,
        relationship_fields=untyped_relationship_fields,
    )
