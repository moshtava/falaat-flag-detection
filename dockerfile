FROM python:3.12.4-slim

ARG USERNAME
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV PYTHONUNBUFFERED=${PYTHONUNBUFFERED}

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        git \
        curl \
        build-essential \
        libpq-dev \
        sudo \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/lib/apt/lists/partial

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --default-timeout=100 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && pip3 install daphne \
    && rm -rf /tmp/pip-tmp

WORKDIR /workspace

COPY . /workspace/

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

SHELL ["/bin/bash", "-c"]

RUN chown -R ${USERNAME}:${USERNAME} /workspace

USER ${USERNAME}

RUN echo '#!/bin/bash\n\
exec daphne -b 0.0.0.0 -p 8000 config.asgi:application' \
> /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
