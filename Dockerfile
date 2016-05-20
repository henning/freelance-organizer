FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y dist-upgrade

RUN apt-get install -y python-virtualenv

RUN mkdir -p /opt/freelance-organizer

RUN virtualenv -p $(which python3) /opt/freelance-organizer/venv
ADD requirements.txt /tmp/
RUN /opt/freelance-organizer/venv/bin/pip install -r /tmp/requirements.txt

ADD . /opt/freelance-organizer/app

WORKDIR /opt/freelance-organizer/app

EXPOSE 8000

ENTRYPOINT ["./docker-run.sh"]
