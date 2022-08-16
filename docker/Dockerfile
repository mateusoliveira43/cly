FROM python:3.10.6-bullseye as install-poetry

RUN curl -sSL https://install.python-poetry.org > ./install-poetry.py

FROM python:3.10.6-slim-bullseye as development

ARG GROUP_ID=1000
ARG USER_ID=1000
ARG USER_NAME=develop
ARG WORK_DIR=/home/$USER_NAME/PROJECT

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.1.14 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/usr/bin/poetry \
    PATH=/usr/bin/poetry/bin:$PATH

WORKDIR /
COPY --from=install-poetry ./install-poetry.py ./
RUN python ./install-poetry.py \
    && rm ./install-poetry.py \
    && groupadd --gid $GROUP_ID $USER_NAME \
    && useradd --uid $USER_ID --gid $GROUP_ID --create-home $USER_NAME \
    && runuser --user $USER_NAME -- mkdir $WORK_DIR
USER $USER_NAME

WORKDIR $WORK_DIR
COPY pyproject.toml poetry.lock ./
RUN poetry install
