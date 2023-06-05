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
    if not latest_pids:
        click.echo("No updates in the backoffice!")
        return

    catalogue_site_query = get_full_query(pid=latest_pids, subject=subjects)
    message = get_site_api_docs(catalogue_site_query)
    if message is None:
        click.echo("No results visible in the catalogue!")
        return

    notification_status = send_channel_request(create_channel_message(message))
    if notification_status == 200:
        click.echo("Notification sent successfully!")
        return


if __name__ == "__main__":
    send_notifications()
