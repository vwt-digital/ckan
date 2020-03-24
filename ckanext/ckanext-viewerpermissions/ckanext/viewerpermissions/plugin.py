import ckan.plugins as plugins
from ckan.lib.plugins import DefaultPermissionLabels
from ckan.authz import auth_is_loggedin_user
import os
import logging


log = logging.getLogger(__name__)


class ViewerpermissionsPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):
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
        log.debug("get_dataset_owner called")
        if self.private_orgs:
            log.debug("private orgs env set")
            private_orgs_list = self.private_orgs.split(',')
            labels = []
            if dataset_obj.owner_org in private_orgs_list:
                labels.extend(u'private')
                log.debug("dataset {} label private".format(dataset_obj.owner_org))
            log.debug("dataset {} label public".format(dataset_obj.owner_org))
            labels.extend(u'public')
            log.debug("current dataset labels")
            for label in labels:
                log.debug(label)
            return labels

        log.debug("private orgs env not set")

        return super(ViewerpermissionsPlugin, self).get_dataset_owner(
            dataset_obj)

    def get_user_dataset_labels(self, user_obj):
        u'''
        If a user is logged in, it can view the private and public datasets
        Otherwise only the public datasets
        '''
        log.debug("get_user_dataset_labels called")
        labels = super(ViewerpermissionsPlugin, self
                       ).get_user_dataset_labels(user_obj)
        if auth_is_loggedin_user():
            labels.extend(u'private')
            log.debug("user is logged in")
        else:
            log.debug("user is not logged in")

        labels.extend(u'public')
        log.debug("Current user labels:")
        for label in labels:
            log.debug(label)
        return labels

    def update_config(self, config):
        # Update our configuration
        self.private_orgs = os.environ.get("CKAN_PRIVATE_ORGS", config.get('ckan.viewerpermissions.private_orgs', None))

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        plugins.toolkit.add_template_directory(config, 'templates')
