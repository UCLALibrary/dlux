FROM python:3.13-slim-bookworm AS base

ARG DJANGO_UID=1000

# Set correct timezone
RUN ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime


# Create django user
RUN useradd --comment "django app user" \
            --home-dir /home/django \
            --shell /bin/bash \
            --uid ${DJANGO_UID} \
            --create-home \
            django

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


FROM base AS dev

RUN pip install --no-cache-dir -r requirements-dev.txt --user --no-warn-script-location
ENV DJANGO_RUN_ENV=dev


# put prod last to make it the default build
FROM base AS prod

ENV DJANGO_RUN_ENV=prod

