from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RelationshipField:
    class_name: str
    field_name: str
    field_type: str
    start_line_number: int
    end_line_number: int
    original_code: str
    typed_code: Optional[str] = None


@dataclass
class RelationshipFieldsInFile:
    path: Path
    relationship_fields: list[RelationshipField]
