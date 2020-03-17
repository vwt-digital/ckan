import ckan.plugins as plugins
from ckan.lib.plugins import DefaultPermissionLabels
from ckan.plugins.toolkit import get_action


class Oauth2PermissionsPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):
    plugins.implements(plugins.IPermissionLabels)
    u'''
    Example permission labels plugin that makes datasets whose
    organisation field is of a field that is within VWT visible only to logged-in users.
    '''

    def get_dataset_owner(self, dataset_obj):
        u'''
        Use member-* labels for proposed datasets
        '''
        if dataset_obj.owner_org.startswith(u'dat'):
            labels = [u'member-%s' % dataset_obj.creator_user_id]
            return labels

        return super(Oauth2PermissionsPlugin, self).get_dataset_labels(
            dataset_obj)

    def get_user_dataset_labels(self, user_obj):
        u'''
        If a user has permission member-*, it can view the datasets
        '''
        labels = super(Oauth2PermissionsPlugin, self
                       ).get_user_dataset_labels(user_obj)
        if user_obj:
            orgs = get_action(u'organization_list_for_user')(
                {u'user': user_obj.id}, {u'permission': u'member'})
            labels.extend(u'member-%s' % o['id'] for o in orgs)
        return labels
