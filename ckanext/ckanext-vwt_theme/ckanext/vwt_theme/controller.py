
# encoding: utf-8
'''
    controller.py
'''
import logging
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
from ckan.common import _, g

logger = logging.getLogger(__name__)

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
get_action = logic.get_action

class Vwt_ThemeController(base.BaseController):


    def read(self, dataset_name, resource_id):
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': g.user,
            u'for_view': True,
            u'auth_user_obj': g.userobj
        }
        data_dict = {u'id': dataset_name, u'include_tracking': True}

        # check if package exists
        try:
            pkg_dict = get_action(u'package_show')(context, data_dict)
            pkg = context[u'package']
        except (NotFound, NotAuthorized):
            return base.abort(404, _(u'Dataset not found'))

        # logger.info(json.dumps(pkg_dict, indent=4, sort_keys=False))

        data_dict_res = {u'id': resource_id, u'include_tracking': True}

        # check if resource exists
        try:
            resource_dict = get_action(u'resource_show')(context, data_dict_res)
        except (NotFound, NotAuthorized):
            return base.abort(404, _(u'Resource not found'))

        # logger.info(json.dumps(resource_dict, indent=4, sort_keys=False))

        return base.render(
        u'package/schema.html', {
                                u'package': pkg,
                                u'pkg': pkg,
                                u'pkg_dict': pkg_dict,
                                u'resource': resource_dict,
                                u'current_resource_view': resource_dict
        }
    )
