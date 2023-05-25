"""The command line module containing all the commands to filter documents."""


import click

from .api import make_api_request
from .utils import get_full_query


@click.command()
@click.option(
    "--pid",
    type=click.STRING,
    multiple=True,
    help="The document pid. Example: w4rr3-d4920 ",
)
@click.option(
    "--created",
    type=click.STRING,
    multiple=True,
    help='Date range for created filter in "YYYY-MM-DD:YYYY-MM-DD" format.',
)
@click.option(
    "--subjects",
    type=click.STRING,
    multiple=True,
    help="Subject and/or the scheme. Example: 005*:UDC, 65*",
)
@click.option(
    "--pub-year",
    type=click.STRING,
    multiple=True,
    help='Year range for publication year filter in "YYYY:YYYY" format.',
)
def get_documents_to_notify(pid, created, subjects, pub_year):
    query = get_full_query(pid, created, subjects, pub_year)
    filtered_docs = make_api_request(query)
    click.echo(filtered_docs)


if __name__ == "__main__":
    get_documents_to_notify()
