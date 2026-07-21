FROM debian:bookworm AS base

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

# Install UV
COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

# "activate" the virtualenv
ENV PATH="/home/django/django_app/.venv/bin:$PATH"

# Install requirements for this application
COPY --chown=django:django pyproject.toml uv.lock ./
VOLUME /home/django/django_app/.venv
RUN --mount=type=cache,target=/home/django/.cache/uv,uid=${DJANGO_UID} \
    uv sync --locked --no-dev

# Expose the typical Django port
EXPOSE 8000

# When container starts, run script for environment-specific actions
CMD [ "sh", "docker_scripts/entrypoint.sh" ]


FROM base AS dev

USER root
RUN apt-get update && apt-get install -y git openssh-client && rm -rf /var/lib/apt/lists/*
USER django

# add the dev requirements
RUN --mount=type=cache,target=/home/django/.cache/uv,uid=${DJANGO_UID} \
    uv sync --locked --group=dev
ENV DJANGO_RUN_ENV=dev


# put prod last to make it the default build
FROM base AS prod

ENV DJANGO_RUN_ENV=prod

