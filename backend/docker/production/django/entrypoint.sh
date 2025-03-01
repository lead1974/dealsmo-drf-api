#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

export CELERY_BROKER_URL="${CELERY_BROKER}"

if [ -z "${POSTGRES_USER}" ]; then
  base_postgres_image_default_user='postgres'
  export POSTGRES_USER="${base_postgres_image_default_user}"
fi

export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

# Check if the environment variable CHECK_DB is set
if [ "${CHECK_DB:-}" = "true" ]; then
  /wait-for-it.sh db:5432 --timeout=5 -- echo "PostgreSQL is available"
fi

exec "$@"