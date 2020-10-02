# See CKAN docs on installation from Docker Compose on usage
FROM debian:stretch
MAINTAINER Open Knowledge

# Install required system packages
RUN apt-get -q -y update \
    && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
    && apt-get -q -y install \
        python-dev \
        python-pip \
        python-virtualenv \
        python-wheel \
        python3-dev \
        python3-pip \
        python3-virtualenv \
        python3-wheel \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libgeos-dev \
        libssl-dev \
        libffi-dev \
        postgresql-client \
        build-essential \
        git-core \
        vim \
        wget \
	      redis-server \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*

# Define environment variables
ENV CKAN_HOME /usr/lib/ckan
ENV CKAN_VENV $CKAN_HOME/venv
ENV CKAN_CONFIG /etc/ckan
ENV CKAN_STORAGE_PATH=/var/lib/ckan
ENV GCP=yes

# Build-time variables specified by docker-compose.yml / .env
ARG CKAN_SITE_URL

# Create ckan user
RUN useradd -r -u 900 -m -c "ckan account" -d $CKAN_HOME -s /bin/false ckan

# Setup virtual environment for CKAN
RUN mkdir -p $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    virtualenv $CKAN_VENV && \
    ln -s $CKAN_VENV/bin/pip /usr/local/bin/ckan-pip &&\
    ln -s $CKAN_VENV/bin/paster /usr/local/bin/ckan-paster

# Setup CKAN
ADD . $CKAN_VENV/src/ckan/
RUN ckan-pip install -U pip && \
    ckan-pip install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirement-setuptools.txt && \
    ckan-pip install --upgrade --no-cache-dir -r $CKAN_VENV/src/ckan/requirements.txt && \
    ckan-pip install -e $CKAN_VENV/src/ckan/ && \
    ln -s $CKAN_VENV/src/ckan/ckan/config/who.ini $CKAN_CONFIG/who.ini && \
    # If GCP is used, use entrypoint from docker-GCP folder
    if [ "$GCP" = "yes" ];then \
        cp -v $CKAN_VENV/src/ckan/contrib/docker-GCP/ckan-entrypoint.sh /ckan-entrypoint.sh && \
        # Also add secrets to env file
        CKAN_OAUTH2_CLIENT_SECRET_SECRET_ID=$(grep CKAN_OAUTH2_CLIENT_SECRET_SECRET_ID $CKAN_VENV/src/ckan/contrib/docker-GCP/temp.env | cut -d '=' -f2) && \
        CKAN_SQLALCHEMY_URL_SECRET_ID=$(grep CKAN_SQLALCHEMY_URL_SECRET_ID $CKAN_VENV/src/ckan/contrib/docker-GCP/temp.env | cut -d '=' -f2) && \
        PROJECT_ID=$(grep PROJECT_ID $CKAN_VENV/src/ckan/contrib/docker-GCP/temp.env | cut -d '=' -f2) && \
        ckan-pip install google-cloud-secret-manager==2.0.0 && \
        python $CKAN_VENV/src/ckan/contrib/docker-GCP/cloud-compute-instance/access_secrets.py -ocs $CKAN_OAUTH2_CLIENT_SECRET_SECRET_ID -sus $CKAN_SQLALCHEMY_URL_SECRET_ID -p $PROJECT_ID -f "$CKAN_VENV/src/ckan/contrib/docker-GCP/.env"; \
    else \
        cp -v $CKAN_VENV/src/ckan/contrib/docker/ckan-entrypoint.sh /ckan-entrypoint.sh; \
    fi && \
    chmod +x /ckan-entrypoint.sh && \
    chown -R ckan:ckan $CKAN_HOME $CKAN_VENV $CKAN_CONFIG $CKAN_STORAGE_PATH && \
    . /usr/lib/ckan/venv/bin/activate && \
    cd $CKAN_VENV/src/ckan/ckanext/ckanext-viewerpermissions && \
    python setup.py develop && \
    cd ../ckanext-vwt_theme && \
    python setup.py develop && \
    cd ../ckanext-custom_vocabulary && \
    python setup.py develop && \
    cd ../../../../.. && \
    deactivate

ENTRYPOINT ["/ckan-entrypoint.sh"]

USER ckan
EXPOSE 5000

CMD ["ckan-paster","serve","/etc/ckan/production.ini"]
