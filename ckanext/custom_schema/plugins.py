from ckan.plugins import (
    toolkit,
    IConfigurer,
    IRoutes,
    IPackageController,
    IValidators,
    SingletonPlugin,
    implements,
    toolkit
)

from ckanext.custom_schema.validators import (
    tag_not_empty
)

class customSchema(SingletonPlugin):
    implements(IConfigurer)
    implements(IRoutes,inherit=True)
    implements(IPackageController, inherit=True)
    implements(IValidators)

    def update_config(self, config):
        toolkit.add_public_directory(config, "static")
        toolkit.add_template_directory(config, "templates")
        toolkit.add_resource('fanstatic', 'custom_schema')

        config['scheming.presets'] = """
ckanext.scheming:presets.json
ckanext.custom_schema:schemas/presets.yaml
"""

        config['scheming.dataset_schemas'] = """
ckanext.custom_schema:schemas/dataset.yaml
"""

    def before_map(self,m):
        m.connect(
            '/metadata_download/{package_id}',
            controller='ckanext.custom_schema.controller:CustomSchemaController',
            action='metadata_download'
        )
        return m

    # IPackageController
    def after_create(self, context, pkg_dict):
        if 'group' in pkg_dict:
            if pkg_dict['group']:
                data = {
                    'id': pkg_dict['group'],
                    'object': pkg_dict['id'],
                    'object_type': 'package',
                    'capacity': 'public'
                }
                toolkit.get_action('member_create')(context, data)

    def after_update(self, context, pkg_dict):
        if 'group' in pkg_dict:
            if pkg_dict['group']:
                data = {
                    'id': pkg_dict['group'],
                    'object': pkg_dict['id'],
                    'object_type': 'package',
                    'capacity': 'public'
                }
                toolkit.get_action('member_create')(context, data)
            self.remove_from_other_groups(context, pkg_dict['id'])

    def remove_from_other_groups(self, context, package_id):
        package = toolkit.get_action('package_show')(context, {'id': package_id})
        for group in package['groups']:
            if group['name'] != package['group']:
                toolkit.get_action('member_delete')(context, {'id': group['id'], 'object': package['id'], 'object_type': 'package'})

    def get_validators(self):
        return {
            'tag_not_empty': tag_not_empty
            }
