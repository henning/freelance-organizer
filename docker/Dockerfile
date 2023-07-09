FROM ubuntu:23.04

RUN apt-get update && apt-get -y dist-upgrade

RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install \
    make python3-poetry python3-virtualenv

RUN mkdir -p /opt/freelance-organizer

ADD . /tmp/build
WORKDIR /tmp/build

RUN poetry install
RUN make test

RUN python3 -m virtualenv /opt/freelance-organizer/venv

RUN /opt/freelance-organizer/venv/bin/python3 -m pip install .

WORKDIR /opt/freelance-organizer/
COPY docker/run-app.sh .

RUN rm -rf /tmp/build

ENV DJANGO_SETTINGS_MODULE=freelance_organizer.settings.production

EXPOSE 9000

ENTRYPOINT ["/opt/freelance-organizer/run-app.sh"]
