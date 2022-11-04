#!/bin/bash
docker run -d \
  --name freelance-organizer-localdbtest \
  -v $(pwd):/var/lib/freelance-organizer \
  -p 9999:9000 \
  freelance-organizer:latest
