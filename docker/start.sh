#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [[ $1 == "prod" ]]; then
  alembic upgrade head
elif [[ $1 == 'local' ]]; then
  alembic upgrade head
elif [[ $1 == "celery" ]]; then
  celery -A app.celery_app worker -l DEBUG
fi
