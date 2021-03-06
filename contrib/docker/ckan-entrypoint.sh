#!/bin/sh
set -e

# URL for the primary database, in the format expected by sqlalchemy (required
# unless linked to a container called 'db')
: ${CKAN_SQLALCHEMY_URL:=}
# URL for solr (required unless linked to a container called 'solr')
: ${CKAN_SOLR_URL:=}
# URL for redis (required unless linked to a container called 'redis')
: ${CKAN_REDIS_URL:=}
# URL for datapusher (required unless linked to a container called 'datapusher')
: ${CKAN_DATAPUSHER_URL:=}

CONFIG="${CKAN_CONFIG}/production.ini"

abort () {
  echo "$@" >&2
  exit 1
}

set_environment () {
  export CKAN_SITE_ID=${CKAN_SITE_ID}
  export CKAN_SITE_URL=${CKAN_SITE_URL}
  export CKAN_SQLALCHEMY_URL=${CKAN_SQLALCHEMY_URL}
  export CKAN_SOLR_URL=${CKAN_SOLR_URL}
  export CKAN_REDIS_URL=${CKAN_REDIS_URL}
  export CKAN_STORAGE_PATH=/var/lib/ckan
  export CKAN_DATAPUSHER_URL=${CKAN_DATAPUSHER_URL}
  export CKAN_DATASTORE_WRITE_URL=${CKAN_DATASTORE_WRITE_URL}
  export CKAN_DATASTORE_READ_URL=${CKAN_DATASTORE_READ_URL}
  export CKAN_SMTP_SERVER=${CKAN_SMTP_SERVER}
  export CKAN_SMTP_STARTTLS=${CKAN_SMTP_STARTTLS}
  export CKAN_SMTP_USER=${CKAN_SMTP_USER}
  export CKAN_SMTP_PASSWORD=${CKAN_SMTP_PASSWORD}
  export CKAN_SMTP_MAIL_FROM=${CKAN_SMTP_MAIL_FROM}
  export CKAN_MAX_UPLOAD_SIZE_MB=${CKAN_MAX_UPLOAD_SIZE_MB}

  export CKAN_OAUTH2_AUTHORIZATION_ENDPOINT=${CKAN_OAUTH2_AUTHORIZATION_ENDPOINT}
  export CKAN_OAUTH2_TOKEN_ENDPOINT=${CKAN_OAUTH2_TOKEN_ENDPOINT}
  export CKAN_OAUTH2_CLIENT_ID="${CKAN_OAUTH2_CLIENT_ID}"
  export CKAN_OAUTH2_CLIENT_SECRET="${CKAN_OAUTH2_CLIENT_SECRET}"
  export CKAN_OAUTH2_PROFILE_API_URL=${CKAN_OAUTH2_PROFILE_API_URL}
  export CKAN_OAUTH2_SCOPE="${CKAN_OAUTH2_SCOPE}"
  export CKAN_OAUTH2_PROFILE_API_USER_FIELD=${CKAN_OAUTH2_PROFILE_API_USER_FIELD}
  export CKAN_OAUTH2_PROFILE_API_MAIL_FIELD=${CKAN_OAUTH2_PROFILE_API_MAIL_FIELD}

  export CKAN_PRIVATE_ORGS=${CKAN_PRIVATE_ORGS}

  export OAUTHLIB_INSECURE_TRANSPORT=${OAUTHLIB_INSECURE_TRANSPORT}
  export OAUTHLIB_RELAX_TOKEN_SCOPE=${OAUTHLIB_RELAX_TOKEN_SCOPE}
}

write_config () {
  ckan-paster make-config --no-interactive ckan "$CONFIG"
}

# If we don't already have a config file, bootstrap
if [ ! -e "$CONFIG" ]; then
  write_config
fi

# Get or create CKAN_SQLALCHEMY_URL
if [ -z "$CKAN_SQLALCHEMY_URL" ]; then
  abort "ERROR: no CKAN_SQLALCHEMY_URL specified in docker-compose.yml"
fi

if [ -z "$CKAN_SOLR_URL" ]; then
    abort "ERROR: no CKAN_SOLR_URL specified in docker-compose.yml"
fi

if [ -z "$CKAN_REDIS_URL" ]; then
    abort "ERROR: no CKAN_REDIS_URL specified in docker-compose.yml"
fi

if [ -z "$CKAN_DATAPUSHER_URL" ]; then
    abort "ERROR: no CKAN_DATAPUSHER_URL specified in docker-compose.yml"
fi

set_environment
ckan-paster --plugin=ckan db init -c "${CKAN_CONFIG}/production.ini"
#ckan-paster --plugin=ckan create-test-data --config="${CKAN_CONFIG}/production.ini"
exec "$@"
