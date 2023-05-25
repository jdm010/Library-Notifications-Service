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
    help="Subject and/or the scheme in 'subject_wildcard:subject_scheme'. Example: 005*:UDC, 65*.\n \
         If only one of them available, use 'subject_wildcard:' or ':subject_scheme'",
)
@click.option(
    "--pub-year",
    type=click.STRING,
    multiple=True,
    help='Year range for publication year filter in "YYYY:YYYY" format.',
)
def get_documents_to_notify(pid, created, subjects, pub_year):
    """A CLI command to interact with library catalogue API.

    Supported Parameters: pid, created,  subjects, publication year. \n
    python3 -m src.cli --pub-year 2018:2019 --pub-year 2019:2023 \n
    python3 -m src.cli --pid w4rr3-d4920  --pub-year 2018:2023 \n
    python3 -m src.cli --pub-year 2018:2023 \n
    python3 -m src.cli --pid w4rr3-d4920  --created 2023-04-24:2023-04-28 \n
    python3 -m src.cli --pid w4rr3-d4920  --pid mwd5h-vew74 --created 2023-04-24:2023-04-28 --subjects "005*:UDC" --subjects "65*:" --pub-year 2018:2023 \n
    """
    query = get_full_query(pid, created, subjects, pub_year)
    filtered_docs = make_api_request(query)
    click.echo(filtered_docs)


if __name__ == "__main__":
    get_documents_to_notify()
