"""The command line module containing all the commands to filter documents."""


import click

from .api import make_api_request
from .utils import get_query


@click.command()
@click.option('--created', type=click.STRING, required=True, help='Date range for created filter in "YYYY-MM-DD:YYYY-MM-DD" format.')
@click.option('--pub-year', type=click.STRING, required=True, help='Year range for publication year filter in "YYYY:YYYY" format.')
def get_results(created, pub_year):
    query = get_query(created, pub_year)
    filtered_docs = make_api_request(query)
    click.echo(filtered_docs)


if __name__ == '__main__':
   get_results()
