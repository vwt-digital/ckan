# encoding: utf-8
'''
    plugin.py
'''
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import json

log = logging.getLogger(__name__)


def get_schema_from_resource(resource):
    # Get schema
    if 'schema' in resource:
        schema = resource['schema']
        return schema
    return False


def schema_to_list(schema):
    # Make schema into string if necessary
    if type(schema) is dict:
        schema = json.dumps(schema, indent=2)
    # Make schema into list so that every newline can be printed
    schema_list = schema.split('\n')
    # Replace every whitespace with its html code, otherwise there are no indents
    schema_list = [s.replace(" ", "&nbsp;") for s in schema_list]
    return schema_list


def get_schema_title(schema):
    # Convert unicode to json
    # Get schema title from json
    if type(schema) is unicode:  # noqa: F821
        schema = schema.replace("\'", "\"")
        schema_json = json.loads(schema)
        schema_title = schema_json.get('$id')
    elif type(schema) is dict:
        schema_title = schema.get('$id')
        schema_title = str(schema_title)
    else:
        schema_title = ''
    schema_title_list = schema_title.split(':')
    schema_title_final = schema_title_list[1]
    return schema_title_final


def schema_title_to_url(schema):
    schema_title = get_schema_title(schema)
    schema_title = schema_title.replace("/", "-")
    return schema_title


def schema_title_from_url(schema_title):
    schema_title = schema_title.replace("-", "/")
    return schema_title


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
        return {'vwt_theme_schema_to_list': schema_to_list,
                'vwt_theme_get_schema_title': get_schema_title,
                'vwt_theme_get_schema_from_resource': get_schema_from_resource,
                'vwt_theme_schema_title_to_url': schema_title_to_url,
                'vwt_theme_schema_title_from_url': schema_title_from_url}

    def before_map(self, map):
        controller = 'ckanext.vwt_theme.controller:Vwt_ThemeController'
        map.connect('schema.read', '/dataset/{dataset_name}/resource/{resource_id}/schema/{active_schema_title}',
                    controller=controller, action='read')
        return map

    def after_map(self, map):
        return map
