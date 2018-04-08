#!/bin/bash

set -x

source /etc/bash_completion


cd $(dirname $0)

workon freelance-organizer-production

set -e

pip install -r requirements.txt

#cp db.sqlite3 ~/tmp/backups/db.sqlite3_$(date +%Y-%m-%d_%s)
source db-tmp-backup.sh

./manage.py runserver 8888 2>&1 >>production.log
