#!/bin/bash
set -eo pipefail
rm -f db.sqlite3
python manage.py migrate
python manage.py initgroups
python manage.py loaddata superuser users components