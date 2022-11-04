FROM ubuntu:19.10

RUN apt-get update
RUN apt-get -y dist-upgrade

RUN apt-get install -y python-virtualenv

RUN mkdir -p /opt/freelance-organizer

RUN virtualenv -p $(which python3) /opt/freelance-organizer/venv
ADD requirements.txt /tmp/
RUN /opt/freelance-organizer/venv/bin/pip install -r /tmp/requirements.txt

ADD . /opt/freelance-organizer/app

WORKDIR /opt/freelance-organizer/app

ENV DJANGO_SETTINGS_MODULE=freelance_organizer.settings.production

EXPOSE 9000

ENTRYPOINT ["./docker-run.sh"]
