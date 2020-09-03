# encoding: utf-8
'''
    plugin.py
'''
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import json
import ast

log = logging.getLogger(__name__)


def get_schemas(schemas):
    # Get schemas from schema list
    schemas = ast.literal_eval(schemas)
    schemas_list = []
    for s in schemas:
        schemas_list.append(s)
    return schemas_list


def schema_to_list(schema):
    # Make schema into list so that every newline can be printed
    schema_list = schema.split('\n')
    # Replace every whitespace with its html code, otherwise there are no indents
    schema_list = [s.replace(" ", "&nbsp;") for s in schema_list]
    return schema_list


def get_schema_title(schema):
    # Convert unicode to json
    #schema_json = json.loads(schema)
    log.info("schema")
    log.info(schema)
    # Get schema title from json
    schema_title = schema.get('$id')
    log.info("Schema title")
    log.info(schema_title)
    schema_title_list = schema_title.split(':')
    schema_title_final = schema_title_list[1]
    return schema_title_final


class Vwt_ThemePlugin(plugins.SingletonPlugin):
    '''
        The code to use the VWT theme for CKAN.
    '''
    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)

    # Declare that this plugin will implement IRoutes.
    plugins.implements(plugins.IRoutes)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.

        toolkit.add_template_directory(config, 'templates')

    def get_helpers(self):
        '''Register helper functions. '''

        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'vwt_theme_get_schemas': get_schemas,
                'vwt_theme_schema_to_list': schema_to_list,
                'vwt_theme_get_schema_title': get_schema_title}

    def before_map(self, map):
        controller = 'ckanext.vwt_theme.controller:Vwt_ThemeController'
        map.connect('schema.read', '/dataset/{dataset_name}/resource/{resource_id}/schema',
            controller=controller, action='read')
        return map

    def after_map(self, map):
        return map
