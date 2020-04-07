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
is added as well as the `rule <https://github.com/vwt-digital/ckan/tree/develop/ckanext/ckanext-viewerpermissions>`_ 
that only authenticated users can see certain datasets.

Local Installation
------------

To run this CKAN setup locally, use the 
`CKAN installation instructions for Docker 
compose <https://docs.ckan.org/en/2.8/maintaining/installing/install-from-docker-compose.html>`_
in the folder `contrib/docker <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_.

**Note:** CKAN cannot be run locally yet via Docker compose in the folder 
`contrib/docker-GCP <https://github.com/vwt-digital/ckan/tree/develop/contrib/docker>`_.

Google Cloud Platform Installation
------------

To run this CKAN setup on `Google Cloud Platform (GCP) <https://cloud.google.com>`_ build the container image via the 
`Dockerfile <https://github.com/vwt-digital/ckan/blob/develop/Dockerfile>`_ and push it to GCP.
For more information see 
`Build Using Dockerfile <https://cloud.google.com/cloud-build/docs/quickstart-build#build_using_dockerfile>`_.

Environment Variables
------------

The following environment variables need to be set. See the github of 
`ckanext-oauth2 <https://github.com/conwetlab/ckanext-oauth2/wiki/Activating-and-Installing>_` for more information.

**Locally:** in the .env file in contrib/docker:
::
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
        CKAN_PRIVATE_ORGS='organisation1,organisation2,etcetera'

**Note:** Organisations are being segregated by a comma (',').

**GCP:** the same values that have to be added to the .env file above have to be added as environment
variables to the Docker image. With addition:
::
        CKAN_SQLALCHEMY_URL=postgresql://{GCP_DATABASE_USER}:{GCP_DATABASE_PASSWORD}@/{GCP_DATABASE_NAME}?host=/cloudsql/{GCP_INSTANCE}

**Note:** the following also needs to be added to the .env file in contrib/docker-GCP when wanting to run that one locally.
::
        GCP_SQL_INSTANCE

Updating CKAN
------------

When updating CKAN, note that there are `stable versions <https://github.com/ckan/ckan/releases>_`. 
The `master branch <https://github.com/ckan/ckan>_` can be unstable.

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
