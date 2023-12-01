from pathlib import Path


class LinterCLIApplication:
    file_paths: list[Path]
    fix: bool

    def __init__(self, file_paths: list[Path], fix: bool, *args, **kwargs) -> None:
        self.file_paths = file_paths
        self.fix = fix

    def run(self, multi_process: bool, *args, **kwargs) -> None:
        raise NotImplementedError("This is an abstract method")
