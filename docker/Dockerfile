FROM python:3.10.4-bullseye

ARG USER_ID
ARG GROUP_ID
ENV USERNAME python-cli-script-template
ENV HOME /home/$USERNAME
ENV WORKDIR $HOME/$USERNAME
ENV PATH $HOME/.local/bin:$PATH

RUN groupadd --gid $GROUP_ID $USERNAME
RUN useradd --uid $USER_ID --gid $GROUP_ID --create-home $USERNAME
USER $USERNAME

RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.in-project true

RUN mkdir $WORKDIR
WORKDIR $WORKDIR

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
