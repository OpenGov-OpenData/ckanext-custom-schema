import StringIO
import unicodecsv as csv

import ckan.plugins as p
import ckan.lib.base as base
import ckan.model as model

from ckan.common import request
from ckan.plugins.toolkit import (
    ObjectNotFound,
    NotAuthorized,
    get_action,
    _,
    response,
    abort,
    c
)
from pylons import config
from ckanext.scheming import helpers


class CustomSchemaController(base.BaseController):
    def metadata_download(self, package_id):
        context = {
            'model': model,
            'session': model.Session,
            'user': p.toolkit.c.user
        }

        data_dict = {
            'id': package_id,
        }
        try:
            result = get_action('package_show')(context, data_dict)
        except (ObjectNotFound, NotAuthorized):
            abort(404, _('Package not found'))

        dataset_fields = helpers.scheming_get_dataset_schema("dataset")['dataset_fields']
        if hasattr(response, u'headers'):
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-disposition'] = \
            'attachment; filename="{name}-metadata.csv"'.format(name=package_id)

        f = StringIO.StringIO()
        wr = csv.writer(f, encoding='utf-8')

        header = ['Field','Value']
        wr.writerow(header)

        for field in dataset_fields:
            if field['field_name'] == 'tag_string':
                value = self.get_package_tags(result.get('tags'))
                wr.writerow([helpers.scheming_language_text(field['label']),value])
            elif field['field_name'] == 'owner_org':
                org_alias = str(config.get('ckan.organization_alias', 'Organization'))
                wr.writerow([org_alias,result['organization']['title']])
            elif field['field_name'] == 'groups':
                group_alias = str(config.get('ckan.group_alias', 'Group'))+'s'
                value = self.get_package_groups(result.get('groups'))
                wr.writerow([group_alias,value])
            elif helpers.scheming_field_choices(field):
                value = helpers.scheming_choices_label(helpers.scheming_field_choices(field),result.get(field['field_name']))
                wr.writerow([helpers.scheming_language_text(field['label']),value])
            else:
                wr.writerow([helpers.scheming_language_text(field['label']),result.get(field['field_name'])])

        return f.getvalue()

    def get_package_groups(self,groups_dict):
        """
        Build out the group names comma separated string
        """
        groups = [group.get('display_name') for group in groups_dict]
        return ",".join(groups)

    def get_package_tags(self,tags_dict):
        """
        Build out the tag names comma separated string
        """
        tags = [tag.get('display_name') for tag in tags_dict]
        return ",".join(tags)

    def get_package_extrafields(self,extras_list):
        """
        Build out the dict object of the custom fields ie key and value
        """
        custom_fields = {}
        for custom_field in extras_list:
            custom_fields[custom_field["key"]] = custom_field["value"]
        return custom_fields
