FROM python:3.13-slim-bookworm

RUN apt-get update

# Set correct timezone
RUN ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

# Install dependencies needed to build psycopg python module, for
# connection to our standard postgresql databases.
RUN apt-get install -y gcc python3-dev libpq-dev

# Create django user
RUN useradd -c "django app user" -d /home/django -s /bin/bash -m django

# Switch to application directory, creating it if needed
WORKDIR /home/django/django_app

# Make sure django owns app directory, if WORKDIR created it:
# https://github.com/docker/docs/issues/13574
RUN chown -R django:django /home/django

# Change context to django user for remaining steps
USER django

# Copy application files to image, and ensure django user owns everything
COPY --chown=django:django . .

# Include local python bin into django user's path, mostly for pip
ENV PATH=/home/django/.local/bin:${PATH}

# Make sure pip is up to date, and don't complain if it isn't yet
RUN pip install --upgrade pip --disable-pip-version-check

# Install requirements for this application
RUN pip install --no-cache-dir -r requirements.txt --user --no-warn-script-location

# Expose the typical Django port
EXPOSE 8000

# When container starts, run script for environment-specific actions
CMD [ "sh", "docker_scripts/entrypoint.sh" ]
