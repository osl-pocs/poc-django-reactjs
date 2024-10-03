# ref: https://github.com/mamba-org/micromamba-docker/blob/main/Dockerfile

FROM condaforge/mambaforge:latest

LABEL maintainer="Ivan Ogasawara <ivan.ogasawara@gmail.com>"
LABEL org.opencontainers.image.title="PoC Django ReactJS"
LABEL org.opencontainers.image.authors="PoC Django ReactJS Team"
LABEL org.opencontainers.image.source="https://github.com/mentalhealthai-org/poc-django-reactjs"
LABEL org.opencontainers.image.version="latest"
LABEL org.opencontainers.image.description="PoC Django ReactJS Web"
LABEL org.mentalhealthai_org.config.version="latest"

# it is the default, but using it here to have it explicitly
USER root

SHELL ["/bin/bash", "-c"]
# Use bash in Dockerfile RUN commands and make sure bashrc is sourced when
# executing commands with /bin/bash -c
# Needed to have the micromamba activate command configured etc.

ENV ENV_NAME=poc-django-reactjs
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ARG UID=1000
ARG GID=1000

RUN apt-get update -y \
  && apt-get install -y \
    apt-utils \
    build-essential \
    curl \
    tini \
    nginx \
    snapd \
    sudo \
    tzdata \
    gcc-multilib \
    g++-multilib \
    openssl \
  && rm -rf /var/lib/apt/lists/* \
    /var/cache/apt/archives \
    /tmp/*

ENV USERNAME=poc

RUN addgroup --gid ${GID} ${USERNAME} \
  && useradd --uid ${UID} --gid ${GID} -ms /bin/bash ${USERNAME} \
  && mkdir -p /opt/services/poc-django-reactjs \
  && chmod -R a+rwx /opt/conda /opt/services \
  && export ENV_NAME="$ENV_NAME" \
  && chown ${USERNAME}:${USERNAME} /opt/services \
  && echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/poc-django-reactjs \
  && chmod 0440 /etc/sudoers.d/poc-django-reactjs

USER ${USERNAME}

WORKDIR /opt/services/poc-django-reactjs

COPY --chown=${USERNAME}:${USERNAME} ./conda/ /tmp/conda
# COPY --chown=poc-django-reactjs:poc-django-reactjs ./.github/workflows/.condarc /home/poc-django-reactjs/.condarc

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN mamba env create -n $ENV_NAME --file /tmp/conda/base.yaml \
  && mamba env update -n $ENV_NAME --file /tmp/conda/service-linux-extra.yaml \
  && conda clean --all \
  && find /opt/conda/ -type f,l -name '*.pyc' -delete \
  && find /opt/conda/ -type f,l -name '*.js.map' -delete \
  && rm -rf /opt/conda/pkgs /tmp/*

ENV CONDA_PREFIX /opt/conda/envs/$ENV_NAME
ENV PATH ${CONDA_PREFIX}/bin:$PATH

# install dependencies
COPY --chown=poc-django-reactjs:poc-django-reactjs pyproject.toml poetry.lock /opt/services/poc-django-reactjs/
COPY --chown=poc-django-reactjs:poc-django-reactjs containers/poc-django-reactjs/scripts/install-deps.sh /tmp/install-deps.sh

ARG ENV=prod

RUN /tmp/install-deps.sh

COPY --chown=poc-django-reactjs:poc-django-reactjs containers/poc-django-reactjs/scripts/entrypoint.sh /opt/entrypoint.sh
COPY --chown=poc-django-reactjs:poc-django-reactjs src/ /opt/services/poc-django-reactjs/src

# copy start script
COPY --chown=poc-django-reactjs:poc-django-reactjs containers/poc-django-reactjs/scripts/start.sh /opt/start.sh

RUN chmod +x /opt/start.sh \
  && chmod +x /opt/entrypoint.sh \
  && echo "source /opt/entrypoint.sh" > ~/.bashrc

ARG STATIC_ROOT
ARG MEDIA_ROOT
ARG DOCKER_VOLUME_CONTAINER_PATH

ENV STATIC_ROOT ${STATIC_ROOT}
ENV MEDIA_ROOT ${MEDIA_ROOT}
ENV DOCKER_VOLUME_CONTAINER_PATH ${DOCKER_VOLUME_CONTAINER_PATH}

RUN mkdir -p ${DOCKER_VOLUME_CONTAINER_PATH}/data \
  && mkdir -p ${DOCKER_VOLUME_CONTAINER_PATH}/articles \
  && mkdir -p ${DOCKER_VOLUME_CONTAINER_PATH}/plot \
  && mkdir -p ${STATIC_ROOT}/.well-known/acme-challenge \
  && mkdir -p ${MEDIA_ROOT}

WORKDIR /opt/services/poc-django-reactjs/src

ENV PYTHONPATH='/opt/services/poc-django-reactjs/src'

ENTRYPOINT ["tini", "--", "/opt/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

COPY ./containers/compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./containers/compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY ./containers/compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./containers/compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./containers/compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


# copy application code to WORKDIR
COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
