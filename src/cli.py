"""The command line module containing all the commands to filter documents."""


import click

from .api import get_backoffice_latest_pids, get_site_api_docs, send_channel_request
from .utils import create_channel_message, get_full_query


@click.command()
@click.option(
    "--subjects",
    type=click.STRING,
    multiple=True,
    help="Subjects domain. For eg. --subjects 005*:UDC --subjects 65*:",
)
def send_notifications(subjects):
    """A CLI command to send notifications for library updates.

    The created range is last 7 days from running the job.
    The published year is last 5 years from running the job.

    Supported Parameters: subjects \n
    python3 -m src.cli --subjects "005*:UDC" --subjects "65*:" \n
    """
    latest_pids = get_backoffice_latest_pids()
    filtered_docs = get_site_api_docs(get_full_query(pid=latest_pids, subject=subjects))
    notification = send_channel_request(create_channel_message(filtered_docs))
    if notification == 200:
        click.echo("Notification sent successfully!")


if __name__ == "__main__":
    send_notifications()
