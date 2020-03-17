import ckan.plugins as plugins
from ckan.lib.plugins import DefaultPermissionLabels


class Oauth2PermissionsPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):
    plugins.implements(plugins.IPermissionLabels)
    u'''
    Example permission labels plugin that makes datasets whose
    organisation field is of a field that is within VWT visible only to logged-in users.
    '''

    def get_dataset_owner(self, dataset_obj):
        u'''
        Use member-* creator-* and admin-* labels for proposed datasets
        '''
        if dataset_obj.owner_org.startswith(u'dat'):
            labels = [u'member', u'creator', u'admin']
            return labels

        return super(Oauth2PermissionsPlugin, self).get_dataset_labels(
            dataset_obj)

    def get_user_dataset_labels(self, user_obj):
        u'''
        If a user has permission member-*, creator-* or admin-* it can view the datasets
        '''
        labels = super(Oauth2PermissionsPlugin, self
                       ).get_user_dataset_labels(user_obj)
        if user_obj.role == 'member':
            labels.extend(u'member')
        elif user_obj.role == 'admin':
            labels.extend(u'admin')
        elif user_obj.role == 'editor':
            labels.extend(u'editor')
        return labels
