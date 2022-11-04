#!/bin/bash
docker run -d \
  --name freelance-organizer \
  -v $(pwd):/var/lib/freelance-organizer \
  -p 9000:9000 \
  freelance-organizer:production
