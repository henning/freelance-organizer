#!/bin/bash

if [ -z $1 ]; then
    echo "no version given, using HEAD"
    VERSION='HEAD'
else
    VERSION=$1
fi




#NAME="$(basename $(pwd))_$VERSION"
NAME="freelance_organizer_$VERSION"

git archive $VERSION --prefix=$NAME/ -o $NAME.tar.gz
