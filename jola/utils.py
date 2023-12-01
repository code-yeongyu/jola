from pathlib import Path


def get_source_code(file_path: Path):
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("r") as file:
        return file.read()
