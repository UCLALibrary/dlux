# DLux
This is a Django application for managing digital library metadata.

## Developer Information

### Overview of environment

The development environment requires:
* `git` (at least version 2)
* `docker`(version 25+) and `docker compose` (version 2+)

#### Dev container

This project comes with a basic dev container definition, in `.devcontainer/devcontainer.json`. It's known to work with VS Code,
and may work with other IDEs like PyCharm.  For VS Code, it also installs the Python, Black (formatter), and Flake8 (linter)
extensions.

When prompted by VS Code, click "Reopen in container".  This will (re)build the Django container, `dlux-django`. It will also
(re)build a copy of that container, `vsc-dlux-<long_hash>-uid`, install VS Code development tools & extensions within that container,
and start the `docker compose` system.  VS Code will be connected to the Django container, with all code available for editing in that context.

The project's directory is available within the container at `/home/django/django_app`.

#### PostgreSQL container

The development database is a Docker container running PostgreSQL 16, which matches our deployment environment.

#### Django container

This uses Django 5.2, in a Debian 12 (Bookworm) container running Python 3.13.  All code
runs in the container, so local version of Python does not matter.

The container runs via `docker_scripts/entrypoint.sh`, which
* Updates container with any new requirements, if the image hasn't been rebuilt (DEV environment only).
* Waits for the database to be completely available.  This can take 5-10 seconds, depending on your hardware.
* Applies any pending migrations (DEV environment only).
* Creates a generic Django superuser, if one does not already exist (DEV environment only).
* Loads fixtures to populate lookup tables and to add a few sample records.
* Starts the Django application server.

## Setup
1. Build using docker compose.

   ```$ docker compose build```

2. Bring the system up, with containers running in the background.

   ```$ docker compose up -d```

3. Logs can be viewed, if needed (`-f` to tail logs).

   ```
   $ docker compose logs -f db
   $ docker compose logs -f django
   ```

4. Run commands in the containers, if needed.

   ```
   # Open psql client in the dev database container
   $ docker compose exec db psql -d django_db -U django_db
   # Open a shell in the django container
   $ docker compose exec django bash
   # Django-aware Python shell
   $ docker compose exec django python manage.py shell
   # Apply new migrations without a restart
   $ docker compose exec django python manage.py migrate
   # Populate database with sample data (once it exists...)
   $ docker compose exec django python manage.py loaddata --app DJANGO_APP_NAME FIXTURE_NAME
   ```

5. Connect to the running application via browser

   [Application](http://127.0.0.1:8000) and [Admin](http://127.0.0.1:8000/admin)

6. Edit code locally.  All changes are immediately available in the running container, but if a restart is needed:

   ```$ docker compose restart django```

7. Shut down the system when done.

   ```$ docker compose down```

### Loading data

Add application-specific instructions here.

### Logging

Basic logging is available, with logs captured in `logs/application.log`.  At present, logs from both the custom application code and Django itself are captured.

Logging level is set to `INFO` via `.docker-compose_django.env`.  If there's a regular need/desire for DEBUG level, we can discuss that.

#### How to log

Logging can be used in any Python file in the project.  For example, in `views.py`:
```
# Include the module with other imports
import logging
# Instantiate a logger, generally before any functions in the file
logger = logging.getLogger(__name__)

def my_view():
    logger.info('This is a log message from my_view')

    query_results = SomeModel.objects.all()
    for r in query_results:
        logger.info(f'{r.some_field=}')

    try:
        1/0
    except Exception as e:
        logger.exception('Example exception')

    logger.debug('This DEBUG message only appears if DJANGO_LOG_LEVEL=DEBUG')
```
#### Log format
The current log format includes:
* Level: DEBUG, INFO, WARNING, ERROR, or CRITICAL
* Timestamp via `asctime`
* Logger name: to distinguish between sources of messages (`django` vs the specific application)
* Module: somewhat redundant with logger name
* Message: The main thing being logged


#### Viewing the log
Local development environment: `view logs/application.log`.

In deployed container:
* `/logs/`: see latest 200 lines of the log
* `/logs/nnn`: see latest `nnn` lines of the log

### Testing

Tests focus on code which has significant side effects or implements custom logic.
Run tests in the container:

```$ docker compose exec django python manage.py test```

#### Preparing a release

Our deployment system is triggered by changes to the Helm chart.  Typically, this is done by incrementing `image:tag` (on or near line 9) in `charts/prod-<appname></appname>-values.yaml`.  We use a simple [semantic versioning](https://semver.org/) system:
* Bug fixes: update patch level (e.g., `v1.0.1` to `v1.0.2`)
* Backward compatible functionality changes: update minor level (e.g., `v1.0.1` to `v1.1.0`)
* Breaking changes: update major level (e.g., `v1.0.1` to `v2.0.0`)

In addition to updating version in the Helm chart, update the Release Notes in `release_notes.html`.  Put the latest changes first, following the established format.
