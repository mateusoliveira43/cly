FROM python:3.10.5-slim-bullseye as setup

ARG GROUP_ID=1000
ARG USER_ID=1000
ARG PROJECT_NAME=python-cli-script-template
ARG WORK_DIR=/home/$PROJECT_NAME/$PROJECT_NAME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH=/home/$PROJECT_NAME/.local/bin:$PATH

RUN apt-get update \
    && apt-get --no-install-recommends --yes install \
    # Run apt list package to get available versions
    curl=7.74.* \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid $GROUP_ID $PROJECT_NAME \
    && useradd --uid $USER_ID --gid $GROUP_ID --create-home $PROJECT_NAME
USER $PROJECT_NAME

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python \
    && mkdir $WORK_DIR
WORKDIR $WORK_DIR

FROM setup as install

COPY pyproject.toml poetry.lock ./
RUN poetry install
