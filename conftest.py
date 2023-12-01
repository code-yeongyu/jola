from os import path

import pytest


@pytest.fixture
def from_file():
    def _from_file(path: str) -> str:
        with open(path, "r") as f:
            return f.read()

    return _from_file


@pytest.fixture
def get_path():
    def _get_path(script_path: str, relative_path: str) -> str:
        script_directory_path = path.dirname(path.abspath(script_path))
        file_path = path.join(script_directory_path, relative_path)
        return file_path

    return _get_path
