# encoding: utf-8

import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def create_custom_vocab(name):
    '''Create custom vocab, if it does not exist already.'''

    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        toolkit.get_action('vocabulary_show')(context, {'id': name})
        logging.info("Vocab '{}' already exists, skipping.".format(name))
    except toolkit.ObjectNotFound:
        logging.info("Creating vocab '{}'".format(name))
        toolkit.get_action('vocabulary_create')(context, {'name': name})


def list_custom_vocab(name):
    '''Return the list of tags from a custom vocabulary.'''

    create_custom_vocab(name)
    try:
        return toolkit.get_action('tag_list')(data_dict={'vocabulary_id': name})
    except toolkit.ObjectNotFound:
        return None


def domains():
    '''Return the list of domains from the domain vocabulary.'''
    return list_custom_vocab('domain')


def solutions():
    '''Return the list of solutions from the solution vocabulary.'''
    return list_custom_vocab('solution')


class Custom_VocabularyPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''A custom vocab plugin.'''

    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)

    def dataset_facets(self, facets_dict, package_type):
        facets_dict['vocab_domain'] = plugins.toolkit._('Domains')
        facets_dict['vocab_solution'] = plugins.toolkit._('Solutions')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def get_helpers(self):
        return {'domains': domains, 'solutions': solutions}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        schema.update({
            'domain': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_tags')('domains')],
            'solution': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_tags')('solutions')]
        })
        return schema

    def create_package_schema(self):
        schema = super(Custom_VocabularyPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(Custom_VocabularyPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(Custom_VocabularyPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'domain': [toolkit.get_converter('convert_from_tags')('domains'), toolkit.get_validator('ignore_missing')],
            'solution': [toolkit.get_converter('convert_from_tags')('solutions'), toolkit.get_validator('ignore_missing')]
        })
        return schema
