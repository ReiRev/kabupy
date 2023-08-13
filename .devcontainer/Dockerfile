FROM mcr.microsoft.com/devcontainers/python:3.11

RUN python -m pip install --upgrade pip \
    && python -m pip install 'flit>=3.8.0'\
    && python -m pip install 'tox==4.7.0'

ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH
RUN curl https://pyenv.run | bash \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc \
    && eval "$(pyenv init -)"
RUN pyenv install 3.10.12
ENV PATH $PATH:/.pyenv/versions/3.10.12/bin
RUN pyenv install 3.9.17
ENV PATH $PATH:/.pyenv/versions/3.9.17/bin
RUN pyenv install 3.8.17
ENV PATH $PATH:/.pyenv/versions/3.8.17/bin

ENV FLIT_ROOT_INSTALL=1

COPY pyproject.toml .
RUN touch README.md \
    && mkdir -p src/kabupy \
    && python -m flit install --only-deps --deps develop \
    && rm -r pyproject.toml README.md src
