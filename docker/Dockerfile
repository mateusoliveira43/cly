FROM python:3.10.4-bullseye

ENV PATH /root/.local/bin:$PATH
RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.in-project true

WORKDIR /python-cli-script-template

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
