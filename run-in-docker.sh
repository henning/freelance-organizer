#! /bin/bash


# TODO: ensure virtualenv is up to date

#APPDIR=/opt/freelance-organizer
#VENVDIR=$APPDIR/venv
#VENVDIR=venv

#if ! [ -d $VENVDIR ];
#  virtualenv $VENVDIR -p python2 
#fi

#source $VENVDIR/bin/activate

#pip install -r requirements.lock.txt

  #--expose 9000 \
DOCKER_BASE_CMD="docker run -d \
  -v $(pwd):/opt/freelance-organizer \
  -p 9000:9000 \
  -w /opt/freelance-organizer \
  django:1.9.8"

$DOCKER_BASE_CMD /bin/bash
  
DJANGO_MANAGE="$DOCKER_BASE_CMD \
  python manage.py"

# TODO: save db for saftey...
#$DJANGO_MANAGE migrate

$DJANGO_MANAGE runserver 0.0.0.0:9000
