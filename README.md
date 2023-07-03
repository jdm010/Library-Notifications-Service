# Library Notifications Service

## Development steps

1. Clone the repository.
2. Move to the cloned repository.
3. Create a virtual environment. For example `env` : `python3 -m venv env`.
4. Install `requirements.txt`: `pip install -r requirements.txt`
5. Run the base command and explore options available. `python3 -m src.cli --help`

## Supported Arguments

1. Subjects domain
    - Get the latest(weekly) updates from backoffice and send the notifications for those present in the catalouge.
    - Format: `value:scheme`

2. Title
    - Title of the notification
    - Format: `'Information Technology'`

3. Target Group
    - Egroup identifier for sending targetted notifications.
    - Format: `'library-newsletter-notif-it'`

## Adding a new query to send notifications

Add a new container with the required arguments (subject, title, target) in the below mentioned format in `cronjob.yml` in qa/prod environment.

```yaml
-  name: <lns-subject>
   image: registry.cern.ch/cern-sis/library-notifications-service
   envFrom:
    - secretRef:
        name: lns-creds
    - configMapRef:
        name: lns-cfg
    args:
    - '--subjects'
    - '<value:scheme>'
    - '--title'
    - '<string>'
    - '--target'
    - '<e-group-identifier>'
```

## Repository Structure

1. api.py - Module containing calls to library catalouge, backoffice and notifications instances.
2. cli.py - Main module conatining the supported command line arguments.
3. utils.py - Module containing helper methods to manipulate data.
