#!/bin/bash
set -eo pipefail
rm -f catalogue/migrations/0*.py
rm -f db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata superuser
