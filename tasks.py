from invoke.context import Context
from invoke.tasks import task
from rich import print


@task
def format(c: Context):
    c.run("pyupgrade --py39-plus */**/*.py", pty=True)
    c.run("ruff --unsafe-fixes --fix .", pty=True)
    c.run("ruff format .", pty=True)


@task
def check_code(c: Context):
    print("Running [green bold]ruff[/green bold] ...")
    c.run(
        "ruff --unsafe-fixes .",
        pty=True,
    )
    print("\nRunning [green bold]mypy[/green bold] ...")
    c.run("mypy .", pty=True)
    print("\nRunning [green bold]pytest[/green bold] ...")
    c.run("pytest .", pty=True)
