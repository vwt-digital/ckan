import ckan.plugins as plugins
from ckan.lib.plugins import DefaultPermissionLabels
from ckan.authz import auth_is_loggedin_user
import os
import logging

log = logging.getLogger(__name__)


class ViewerpermissionsPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):
    plugins.implements(plugins.IPermissionLabels)
    plugins.implements(plugins.IConfigurer)
    u'''
    Example permission labels plugin that makes datasets whose
    organisation field is of a field that is within VWT visible only to logged-in users.
    '''

    def get_dataset_labels(self, dataset_obj):
        u'''
        If the dataset owner can be found in private organisations, return private and public label
        Otherwise only return public
        '''
        log.debug("get_dataset_labels called")
        private_orgs_list = self.private_orgs.split(',')
        # Get name of organisation
        org_name = dataset_obj.organization.name
        log.debug(org_name)
        labels = []
        label = ''
        # If organisation is private
        if org_name in private_orgs_list:
            # Add 'private' to label
            label = label + 'private'
        # Always add 'public' to label
        label = label + ' public'
        labels = labels + [unicode(label)]  # noqa: F821
        return labels

    def get_user_dataset_labels(self, user_obj):
        u'''
        If a user is logged in, it can view the private and public datasets
        Otherwise only the public datasets
        '''
        log.debug("get_user_dataset_labels called")

        labels = super(ViewerpermissionsPlugin, self
                       ).get_user_dataset_labels(user_obj)
        label = ''
        # If user is logged in
        if auth_is_loggedin_user():
            # Allow access to private datasets
            label = label + 'private'
        # Always allow access to public datasets
        label = label + ' public'
        labels = labels + [unicode(label)]  # noqa: F821
        return labels

    def update_config(self, config):
        # Update our configuration
        self.private_orgs = os.environ.get("CKAN_PRIVATE_ORGS", config.get('ckan.viewerpermissions.private_orgs', None))

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        plugins.toolkit.add_template_directory(config, 'templates')
