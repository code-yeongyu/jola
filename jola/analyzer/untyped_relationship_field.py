import ast

from jola.models import RelationshipField

RELATIONSHIP_FIELD_TYPES = ["ForeignKey", "OneToOneField"]


class UntypedRelationshipFieldFinder(ast.NodeVisitor):
    def __init__(self):
        self.relationship_fields: list[RelationshipField] = []
        self.current_class_name: str = ""

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.current_class_name = node.name
        for n in node.body:
            self.visit(n)

    def visit_Assign(self, node: ast.Assign) -> None:
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            field_type: str = node.value.func.attr

            if field_type in RELATIONSHIP_FIELD_TYPES:
                for target in node.targets:
                    if not hasattr(target, "annotation") or (
                        hasattr(target.annotation, "slice") and not isinstance(target.annotation.slice, ast.Index)  # type: ignore
                    ):
                        fixable: bool = all(not isinstance(arg, ast.Str) for arg in node.value.args)

                        relationship_field = RelationshipField(
                            class_name=self.current_class_name,
                            field_name=target.id,  # type: ignore
                            field_type=field_type,
                            start_line_number=node.lineno,
                            end_line_number=node.end_lineno or node.lineno,
                            original_code=ast.unparse(node),
                        )
                        if fixable:
                            field_definition_with_type: str = (
                                f"{target.id}: "  # type: ignore
                                f"{ast.unparse(node.value.func)}[{node.value.args[0].id}] "  # type: ignore
                                f"= {ast.unparse(node.value)}"
                            )
                            relationship_field.typed_code = field_definition_with_type

                        self.relationship_fields.append(relationship_field)


def find_untyped_relationship_fields(source_code: str) -> list[RelationshipField]:
    tree = ast.parse(source_code)
    finder = UntypedRelationshipFieldFinder()
    finder.visit(tree)
    return finder.relationship_fields
