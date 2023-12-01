from jola.models.relationship_field import RelationshipField


def fix_untyped_relationship_field(
    source_code: str,
    relationship_fields: list[RelationshipField],
) -> str:
    TEMPORARY_REPLACEMENT = "[will be fixed by django-model-generic-linter]"
    lines = source_code.splitlines()
    for field in relationship_fields:
        if field.typed_code:
            indent = len(lines[field.start_line_number - 1]) - len(lines[field.start_line_number - 1].lstrip())
            typed_code_with_indent = field.typed_code.rjust(len(field.typed_code) + indent)
            for i in range(field.start_line_number - 1, field.end_line_number):
                lines[i] = TEMPORARY_REPLACEMENT
            lines[field.start_line_number - 1] = typed_code_with_indent

    lines = [line for line in lines if line.strip() != TEMPORARY_REPLACEMENT]

    new_source_code = "\n".join(lines) + "\n"
    if new_source_code.strip() != source_code.strip():
        return new_source_code
    return source_code
