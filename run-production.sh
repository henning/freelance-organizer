#!/bin/bash

# DB_DIR=/Users/henning/Library/FreelanceOrganizer
DB_DIR=/home/henning/data/produktion/freelance-organizer/prod-db

docker run -d \
  --restart yes \
  --name freelance-organizer \
  -v $DB_DIR:/var/lib/freelance-organizer \
  -p 9000:9000 \
  freelance-organizer:production