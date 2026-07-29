#!/bin/bash

# Write python output in real time without buffering
export PYTHONUNBUFFERED=1

# Pick up any local changes to requirements.txt, which do *not* automatically get re-installed when starting the container.
# Do this only in dev environment!
if [ "$DJANGO_RUN_ENV" = "dev" ]; then
  pip install --no-cache-dir -r requirements.txt --user --no-warn-script-location
fi

# Check when database is ready for connections
echo "Checking database connectivity..."
until python -c 'import os, psycopg ; conn = psycopg.connect(host=os.environ.get("DJANGO_DB_HOST"),port=os.environ.get("DJANGO_DB_PORT"),user=os.environ.get("DJANGO_DB_USER"),password=os.environ.get("DJANGO_DB_PASSWORD"),dbname=os.environ.get("DJANGO_DB_NAME"))' ; do
  echo "Database connection not ready - waiting"
  sleep 5
done

# Run database migrations
python manage.py migrate

##### HISTORY: If django-simple-history is used, enable the block below. #####
# if [ "$DJANGO_RUN_ENV" = "dev" ]; then
#   # Auto-populate history records; may not be needed, but does no harm in dev environment.
#   # Logs will show this message, which is OK:
#   # Existing history found, skipping model <app specific info>
#   python manage.py populate_history --auto
# fi
#### END HISTORY #####

if [ "$DJANGO_RUN_ENV" = "dev" ]; then
  # Create default superuser for dev environment, using django env vars.
  # Logs will show error if this exists, which is OK.
  python manage.py createsuperuser --no-input

  ##### FIXTURES: Enable and add as needed. #####
  # Load fixtures, only in dev environment.
  # python manage.py loaddata groups_and_permissions.json item_statuses.json
  ##### END FIXTURES #####
fi

if [ "$DJANGO_RUN_ENV" = "dev" ]; then
  python manage.py runserver 0.0.0.0:8000
else
  # Build static files directory, starting fresh each time - do we really need this?
  python manage.py collectstatic --no-input

  # Start the Gunicorn web server
  # Gunicorn cmd line flags:
  # -w number of gunicorn worker processes
  # -b IPADDR:PORT binding
  # -t timeout in seconds; allow 180 seconds, for long-running Excel exports.
  # --access-logfile where to send HTTP access logs (- is stdout)
  export GUNICORN_CMD_ARGS="-w 3 -b 0.0.0.0:8000 -t 180 --access-logfile -"
  gunicorn project.wsgi:application
fi
