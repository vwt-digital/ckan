CKAN: The Open Source Data Portal Software
==========================================

.. image:: https://img.shields.io/badge/license-AGPL-blue.svg?style=flat
    :target: https://opensource.org/licenses/AGPL-3.0
    :alt: License

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat
    :target: http://docs.ckan.org
    :alt: Documentation
.. image:: https://img.shields.io/badge/support-StackOverflow-yellowgreen.svg?style=flat
    :target: https://stackoverflow.com/questions/tagged/ckan
    :alt: Support on StackOverflow

.. image:: https://circleci.com/gh/ckan/ckan.svg?style=shield
    :target: https://circleci.com/gh/ckan/ckan
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/ckan/ckan/badge.svg?branch=master
    :target: https://coveralls.io/github/ckan/ckan?branch=master
    :alt: Coverage Status

.. image:: https://badges.gitter.im/gitterHQ/gitter.svg
    :target: https://gitter.im/ckan/chat
    :alt: Chat on Gitter

**CKAN is the world’s leading open-source data portal platform**.
CKAN makes it easy to publish, share and work with data. It's a data management
system that provides a powerful platform for cataloging, storing and accessing
datasets with a rich front-end, full API (for both data and catalog), visualization
tools and more. Read more at `ckan.org <http://ckan.org/>`_.

Additions
------------

In this CKAN setup, `oauth2 authentication <https://github.com/conwetlab/ckanext-oauth2>`_ 
is added together with the `rule <https://github.com/vwt-digital/ckan/tree/develop/ckanext/ckanext-viewerpermissions>`_ 
that only authenticated users can see certain datasets and the addition of a 
`custom VWT vocabulary <https://github.com/vwt-digital/ckan/tree/develop/ckanext/ckanext-custom_vocabulary>`_ 

Local Installation
------------

To run this CKAN setup locally, use the 
`CKAN installation instructions for Docker 
compose <https://docs.ckan.org/en/2.8/maintaining/installing/install-from-docker-compose.html>`_
in the folder `contrib/docker <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_ if you want to run it 
with a local database. Or in the folder `contrib/docker-GCP <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_ 
if you want to run it with a `Google Cloud Platform (GCP) <https://cloud.google.com>`_ database. And if you want to run it with 
a nginx instance, copy the 
`Docker-compose file <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/cloud-compute-instance/docker-compose.yml>`_ 
into `contrib/docker-GCP <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_ and the 
`deployment.ini_tmpl <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/cloud-compute-instance/deployment.ini_tmpl>`_ 
file into `ckan/config <https://github.com/vwt-digital/ckan/tree/develop/ckan/config>`_.

Furthermore make sure that the 'port' variable in 
`deployment.ini_tmpl <https://github.com/vwt-digital/ckan/blob/develop/ckan/config/deployment.ini_tmpl>`_ is set to the right 
port (probably 5000).

If you want to run CKAN with GCP settings, set the 'GCP' variable in the 
`Dockerfile <https://github.com/vwt-digital/ckan/blob/develop/Dockerfile>`_ to 'yes'.

Google Cloud Platform Cloud Run Installation
------------

To run this CKAN setup on `Google Cloud Platform (GCP) Cloud Run <https://cloud.google.com/run>`_ build the container image via the 
`Dockerfile <https://github.com/vwt-digital/ckan/blob/develop/Dockerfile>`_ and push it to GCP.
For more information see 
`Build Using Dockerfile <https://cloud.google.com/cloud-build/docs/quickstart-build#build_using_dockerfile>`_.
Do not forget to add the environment variables.

Google Cloud Platform Compute Engine Installation
------------

To run this CKAN setup on `Google Cloud Platform (GCP) Compute Engine <https://cloud.google.com/compute>`_ first create a network and then
create firewall-rules on this network to open access to the ssl port and, if you want, the ssh port.
Then create the compute instance, for more information see 
`gcloud compute instance create <https://cloud.google.com/sdk/gcloud/reference/compute/instances/create>`_. 
The `google-cloud-init.yml <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/cloud-compute-instance/google-cloud-init.yml>`_
should be used as the user-data in the metadata-from-file parameter.
Nginx also needs ssl certificates, these are made via google-cloud-init.yml but this does need a 
.cnf file, see `How to create a CSR with OpenSSL <https://www.switch.ch/pki/manage/request/csr-openssl/>`_ 
for more information about creating such a file.

Environment Variables
------------

The following environment variables need to be set. See the github of 
`ckanext-oauth2 <https://github.com/conwetlab/ckanext-oauth2/wiki/Activating-and-Installing>`_ for more information.
If you are using Cloud Run, these variables have to be added as environment variables when deploying the image to GCP.
If you are using Cloud Engine, these variables have to be added as metadata when creating the engine. The 
`google-cloud-init file <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/cloud-compute-instance/google-cloud-init.yml>`_ 
shows what the names of these variables should be.
If you are running CKAN locally, only the .env file is needed, it can be made by copying the 
`.env.template <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/.env.template>`_ file and renaming it to .env.

**Locally:** in the .env file in contrib/docker:
::
        CKAN_SOLR_PASSWORD
        SOLR_PORT
        CKAN_SOLR_URL
        CKAN_OAUTH2_AUTHORIZATION_ENDPOINT
        CKAN_OAUTH2_TOKEN_ENDPOINT
        CKAN_OAUTH2_CLIENT_ID
        CKAN_OAUTH2_CLIENT_SECRET
        CKAN_OAUTH2_SCOPE
        CKAN_OAUTH2_PROFILE_API_URL
        CKAN_OAUTH2_PROFILE_API_USER_FIELD
        CKAN_OAUTH2_PROFILE_API_MAIL_FIELD
        OAUTHLIB_INSECURE_TRANSPORT
        OAUTHLIB_RELAX_TOKEN_SCOPE
        CKAN_PRIVATE_ORGS

Where CKAN_PRIVATE_ORGS are the organisations in CKAN that have datasets that should only be visible to authenticated users.
::
        CKAN_PRIVATE_ORGS=organisation1,organisation2,etcetera

**Note:** Organisations are being segregated by a comma (',').

**Note:** When using GCP, make sure that CKAN_SOLR_PASSWORD is the unhashed password of 
`security.json <https://lucene.apache.org/solr/guide/6_6/basic-authentication-plugin.html>`_. Security.json should 
be placed in contrib/docker-GCP/solr.
To change SOLR's password, the file 
`solr_generate_pass.py <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/solr/solr_generate_pass.py>`_ can be used. 

**Note:** When running locally, make sure that the generated password is set as the solr password in the .env file.

**GCP Cloud Run:** Only the following two values do not have to be added, unless running locally:
::
        SOLR_PORT
        CKAN_SOLR_URL

**GCP Cloud Run + Locally:**
The rest of the values that have to be added to the .env file above have to be added as environment
variables to the Docker image. With addition:
::
        CKAN_SQLALCHEMY_URL=postgresql://{GCP_DATABASE_USER}:{GCP_DATABASE_PASSWORD}@/{GCP_DATABASE_NAME}?host=/cloudsql/{GCP_INSTANCE}

**Note:** the following also needs to be added to the .env file in contrib/docker-GCP when wanting to run that one locally.
::
        GCP_SQL_INSTANCE

**GCP Compute Engine:**
All the necessary variables for the Compute Engine can be found in the 
`google-cloud-init file <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/cloud-compute-instance/google-cloud-init.yml>`_.
Note that this file also makes the .env file. When using nginx, the OAUTHLIB_INSECURE_TRANSPORT variable can be set to false.

Updating CKAN
------------

When updating CKAN, note that there are `stable versions <https://github.com/ckan/ckan/releases>`_. 
The `master branch <https://github.com/ckan/ckan>`_ can be unstable.

The following adjustments should be kept or adjusted properly when merging to a branch from the forked CKAN repository:

- `Dockerfile <https://github.com/vwt-digital/ckan/blob/develop/Dockerfile>`_:
    | The variable 'GCP' which is checked when copying the entrypoint in order to know which entrypoint to copy.
    | The activation of the virtual environment in order to install extensions.
- `deployment.ini_tmpl <https://github.com/vwt-digital/ckan/blob/develop/ckan/config/deployment.ini_tmpl>`_:
    | The changing of the port variable to 8080 (unless running locally, as explained before).
    | The OAuth2 configuration settings (all variables starting with 'ckan.oauth2.') for the oauth2 extension,
    | The 'ckan.viewerpermissions.private_orgs' variable for the viewerpermissions extension.
    | The adding of 'vwt_theme oauth2 viewerpermissions' to the ckan.plugins variable.
- `environment.py <https://github.com/vwt-digital/ckan/blob/develop/ckan/config/environment.py>`_:
    | The adding of previously mentioned variables to the config_from_env_vars function.
- `original docker folder <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_:
    | The environment variables for the extensions in the 
      `entrypoint <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_.
    | Also add these env vars to the 
      `docker compose <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker/docker-compose.yml>`_.
    | And add these env vars to the 
      `env.template <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker/.env.template>`_.
- `GCP docker folder <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker-GCP>`_:
    | **Note:** Don't forget to compare this folder to the contrib/docker folder of the branch you want to merge with.
    | The environment variables for the extensions in the 
      `entrypoint <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/ckan-entrypoint.sh>`_.
    | The startup of the Redis server is also added but this might not be necessary in future versions.
    | The search-index rebuild is necessary in order for the database to refill after the site being down for too long.
    | The `docker compose <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/docker-compose.yml>`_ 
      has been adjusted completely to have a GCP SQL proxy to the SQL database instead of a local database. Also the env 
      vars for the extensions have been added.
    | The environment variables for the extensions have also been added to the 
      `env.template <https://github.com/vwt-digital/ckan/blob/develop/contrib/docker-GCP/.env.template>`_.
      Along with the environment variables to set the GCP SQL database. And the removal of any environment variables 
      used to setup a database locally.

Support
-------
If you need help with CKAN or want to ask a question, use either the
`ckan-dev`_ mailing list or the `CKAN tag on Stack Overflow`_ (try
searching the Stack Overflow and ckan-dev `archives`_ for an answer to your
question first).

If you've found a bug in CKAN, open a new issue on CKAN's `GitHub Issues`_ (try
searching first to see if there's already an issue for your bug).

If you find a potential security vulnerability please email security@ckan.org,
rather than creating a public issue on GitHub.

.. _CKAN tag on Stack Overflow: http://stackoverflow.com/questions/tagged/ckan
.. _archives: https://www.google.com/search?q=%22%5Bckan-dev%5D%22+site%3Alists.okfn.org.
.. _GitHub Issues: https://github.com/ckan/ckan/issues
.. _CKAN chat on Gitter: https://gitter.im/ckan/chat


Contributing to CKAN
--------------------

For contributing to CKAN or its documentation, see
`CONTRIBUTING <https://github.com/ckan/ckan/blob/master/CONTRIBUTING.rst>`_.

Mailing List
~~~~~~~~~~~~

Subscribe to the `ckan-dev`_ mailing list to receive news about upcoming releases and
future plans as well as questions and discussions about CKAN development, deployment, etc.

Community Chat
~~~~~~~~~~~~~~

If you want to talk about CKAN development say hi to the CKAN developers and members of
the CKAN community on the public `CKAN chat on Gitter`_. Gitter is free and open-source;
you can sign in with your GitHub, GitLab, or Twitter account.

The logs for the old `#ckan`_ IRC channel (2014 to 2018) can be found here:
https://github.com/ckan/irc-logs.

Wiki
~~~~

If you've figured out how to do something with CKAN and want to document it for
others, make a new page on the `CKAN wiki`_ and tell us about it on the
ckan-dev mailing list or on Gitter.

.. _ckan-dev: http://lists.okfn.org/mailman/listinfo/ckan-dev
.. _#ckan: http://webchat.freenode.net/?channels=ckan
.. _CKAN Wiki: https://github.com/ckan/ckan/wiki
.. _CKAN chat on Gitter: https://gitter.im/ckan/chat


Copying and License
-------------------

This material is copyright (c) 2006-2018 Open Knowledge Foundation and contributors.

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
