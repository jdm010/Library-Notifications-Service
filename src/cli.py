"""The command line module containing all the commands to filter documents."""


import click

from .api import get_backoffice_latest_pids, get_site_api_docs, send_channel_request
from .utils import create_channel_message, get_full_query, get_last_five_years_range


@click.command()
@click.option(
    "--subjects",
    type=click.STRING,
    multiple=True,
    required=True,
    help="Subjects domain. For eg. --subjects 005*:UDC --subjects 65*:",
)
@click.option(
    "--title",
    type=click.STRING,
    required=True,
    help="Subject title. For eg. --title 'Information Technology'",
)
@click.option(
    "--target",
    type=click.STRING,
    required=True,
    help="Egroup identifier. For eg. --target 'library-newsletter-notif-it'",
)
def send_notifications(subjects, title, target):
    """A CLI command to send notifications for library updates.

    The created range is last 7 days from running the job.
    The published year is last 5 years from running the job.

    Supported Parameters: subjects, title and target group. \n
    python3 -m src.cli --subjects "005*:UDC" --subjects "65*:" --title 'Administration/Management' --target 'library-newsletter-notif-admin-management' \n
    """
    latest_pids = get_backoffice_latest_pids()
    if not latest_pids:
        click.echo("No updates in the backoffice!")
        return

    published = get_last_five_years_range()
    catalogue_site_query = get_full_query(
        pid=latest_pids, pub_year=published, subject=subjects
    )
    message = get_site_api_docs(catalogue_site_query)
    if message is None:
        click.echo("No results visible in the catalogue!")
        return

    notification_status = send_channel_request(
        create_channel_message(message, title), target
    )
    if notification_status == 200:
        click.echo("Notification sent successfully!")
        return


if __name__ == "__main__":
    send_notifications()
