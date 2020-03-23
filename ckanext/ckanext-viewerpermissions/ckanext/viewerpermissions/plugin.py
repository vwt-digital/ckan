import ckan.plugins as plugins
from ckan.lib.plugins import DefaultPermissionLabels
from ckan.authz import auth_is_loggedin_user
import os


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
        print("get_dataset_owner called")
        if self.private_orgs:
            print("private orgs env set")
            labels = []
            if dataset_obj.owner_org in self.private_orgs:
                labels.extend(u'private')
                print("dataset {} label private".format(dataset_obj.owner_org))
            print("dataset {} label public".format(dataset_obj.owner_org))
            labels.extend(u'public')
            return labels

        print("private orgs env not set")

        return super(ViewerpermissionsPlugin, self).get_dataset_labels(
            dataset_obj)

    def get_user_dataset_labels(self, user_obj):
        u'''
        If a user is logged in, it can view the private and public datasets
        Otherwise only the public datasets
        '''
        print("get_user_dataset_labels called")
        labels = super(ViewerpermissionsPlugin, self
                       ).get_user_dataset_labels(user_obj)
        if auth_is_loggedin_user():
            labels.extend(u'private')
            print("user is logged in")
        else:
            print("user is not logged in")

        labels.extend(u'public')
        return labels

    def update_config(self, config):
        # Update our configuration
        self.private_orgs = os.environ.get("CKAN_PRIVATE_ORGS", config.get('ckan.viewerpermissions.private_orgs', None))

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        plugins.toolkit.add_template_directory(config, 'templates')
