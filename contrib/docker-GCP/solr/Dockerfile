FROM solr:6.6.5
MAINTAINER Open Knowledge

ARG SOLR_USER
ARG SOLR_PASSWORD
ENV SOLR_USER $SOLR_USER
ENV SOLR_PASSWORD $SOLR_PASSWORD

# Enviroment
ENV SOLR_CORE ckan

# Create Directories
RUN mkdir -p /opt/solr/server/solr/$SOLR_CORE/conf
RUN mkdir -p /opt/solr/server/solr/$SOLR_CORE/data

# Copy security to container
COPY ./contrib/docker-GCP/solr/security.json /opt/solr/server/solr/

# Adding Files
ADD ./contrib/docker-GCP/solr/solrconfig.xml \
./ckan/config/solr/schema.xml \
https://raw.githubusercontent.com/apache/lucene-solr/releases/lucene-solr/6.6.5/solr/server/solr/configsets/basic_configs/conf/currency.xml \
https://raw.githubusercontent.com/apache/lucene-solr/releases/lucene-solr/6.6.5/solr/server/solr/configsets/basic_configs/conf/synonyms.txt \
https://raw.githubusercontent.com/apache/lucene-solr/releases/lucene-solr/6.6.5/solr/server/solr/configsets/basic_configs/conf/stopwords.txt \
https://raw.githubusercontent.com/apache/lucene-solr/releases/lucene-solr/6.6.5/solr/server/solr/configsets/basic_configs/conf/protwords.txt \
https://raw.githubusercontent.com/apache/lucene-solr/releases/lucene-solr/6.6.5/solr/server/solr/configsets/data_driven_schema_configs/conf/elevate.xml \
/opt/solr/server/solr/$SOLR_CORE/conf/

# Create Core.properties
RUN echo name=$SOLR_CORE > /opt/solr/server/solr/$SOLR_CORE/core.properties

# Giving ownership to Solr

USER root
RUN chown -R $SOLR_USER:$SOLR_PASSWORD /opt/solr/server/solr/$SOLR_CORE
RUN chown -R $SOLR_USER:$SOLR_PASSWORD /opt/solr/server/solr/security.json

# User
USER $SOLR_USER:$SOLR_PASSWORD
