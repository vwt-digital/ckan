.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/vwt-digital/ckanext-viewerpermissions.svg?branch=master
    :target: https://travis-ci.org/vwt-digital/ckanext-viewerpermissions

.. image:: https://coveralls.io/repos/vwt-digital/ckanext-viewerpermissions/badge.svg
  :target: https://coveralls.io/r/vwt-digital/ckanext-viewerpermissions

.. image:: https://img.shields.io/pypi/v/ckanext-viewerpermissions.svg
    :target: https://pypi.org/project/ckanext-viewerpermissions/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/ckanext-viewerpermissions.svg
    :target: https://pypi.org/project/ckanext-viewerpermissions/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/ckanext-viewerpermissions.svg
    :target: https://pypi.org/project/ckanext-viewerpermissions/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/ckanext-viewerpermissions.svg
    :target: https://pypi.org/project/ckanext-viewerpermissions/
    :alt: License

=============
ckanext-viewerpermissions
=============

With this CKAN extension one can set organisations to "private", meaning that they can only be viewed when a user
is authenticated.

------------
Requirements
------------

This extension has been tested with CKAN 2.8.3.


------------
Installation
------------

To install ckanext-viewerpermissions:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-viewerpermissions Python package into your virtual environment::

     cd ckanext-viewerpermissions
     python setup.py develop

.. Replace with pip install ckanext-viewerpermissions if it ever gets on pypi

3. Add ``viewerpermissions`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config settings
---------------

# Set private organisations
ckan.viewerpermissions.private_orgs = "organisation1,organisation2,etcetera"

**Note:* organisations are being segregated by a comma (',').


.. Change the following if the extension gets its own git:
    ----------------------
    Developer installation
    ----------------------

    To install ckanext-viewerpermissions for development, activate your CKAN virtualenv and
    do::

        git clone https://github.com/vwt-digital/ckan/tree/develop/ckanext/ckanext-viewerpermissions.git
        cd ckanext-viewerpermissions
        python setup.py develop
        pip install -r dev-requirements.txt


    -----
    Tests
    -----

    To run the tests, do::

        nosetests --nologcapture --with-pylons=test.ini

    To run the tests and produce a coverage report, first make sure you have
    coverage installed in your virtualenv (``pip install coverage``) then run::

        nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.viewerpermissions --cover-inclusive --cover-erase --cover-tests


    ----------------------------------------
    Releasing a new version of ckanext-viewerpermissions
    ----------------------------------------

    ckanext-viewerpermissions should be available on PyPI as https://pypi.org/project/ckanext-viewerpermissions.
    To publish a new version to PyPI follow these steps:

    1. Update the version number in the ``setup.py`` file.
    See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
    for how to choose version numbers.

    2. Make sure you have the latest version of necessary packages::

        pip install --upgrade setuptools wheel twine

    3. Create a source and binary distributions of the new version::

        python setup.py sdist bdist_wheel && twine check dist/*

    Fix any errors you get.

    4. Upload the source distribution to PyPI::

        twine upload dist/*

    5. Commit any outstanding changes::

        git commit -a

    6. Tag the new release of the project on GitHub with the version number from
    the ``setup.py`` file. For example if the version number in ``setup.py`` is
    0.0.1 then do::

        git tag 0.0.1
        git push --tags
