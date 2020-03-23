import ckan.plugins as plugins
from ckan.lib.plugins import DefaultPermissionLabels
from ckan.authz import auth_is_loggedin_user
# import os

class Oauth2PermissionsPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):
    plugins.implements(plugins.IPermissionLabels)
    u'''
    Example permission labels plugin that makes datasets whose
    organisation field is of a field that is within VWT visible only to logged-in users.
    '''

    def get_dataset_owner(self, dataset_obj):
        u'''
        If the dataset owner can be found in private organisations, return private and public label
        Otherwise only return public
        '''
        # TODO: now but update later to env var:
        privateorgs = ['dat']

        labels = []
        if dataset_obj.owner_org in privateorgs:
            labels.extend(u'private')
            labels.extend(u'public')
            return labels
        else:
            labels.extend(u'public')

        return super(Oauth2PermissionsPlugin, self).get_dataset_labels(
            dataset_obj)

    def get_user_dataset_labels(self, user_obj):
        u'''
        If a user is logged in, it can view the private and public datasets
        Otherwise only the public datasets
        '''
        labels = super(Oauth2PermissionsPlugin, self
                       ).get_user_dataset_labels(user_obj)
        if auth_is_loggedin_user():
            labels.extend(u'private')

        labels.extend(u'public')
        return labels

    # def update_config(self, config):
    #     # Update our configuration
    #     self.privateorgs = os.environ.get("CKAN_PRIVATE_ORGS", config.get('ckan.datasetpermissions.privateorgs', None))

    #     # Add this plugin's templates dir to CKAN's extra_template_paths, so
    #     # that CKAN will use this plugin's custom templates.
    #     plugins.toolkit.add_template_directory(config, 'templates')
