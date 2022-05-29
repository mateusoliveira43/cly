FROM python:3.10.4-bullseye

ARG USER_ID
ARG GROUP_ID
ARG USERNAME
ARG WORK_DIR

RUN groupadd --gid $GROUP_ID $USERNAME \
    && useradd --uid $USER_ID --gid $GROUP_ID --create-home $USERNAME
USER $USERNAME

ENV PATH /home/$USERNAME/.local/bin:$PATH
RUN pip install poetry==1.1.13 \
    && poetry config virtualenvs.in-project true \
    && mkdir $WORK_DIR
WORKDIR $WORK_DIR

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
