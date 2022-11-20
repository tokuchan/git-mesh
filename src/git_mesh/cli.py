import logging
import sh
import click

from rich import print
from rich.traceback import install
install(show_locals=True)

@click.group
def cli():
    print("Hello world!")
