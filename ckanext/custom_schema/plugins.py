from ckan.plugins import (
    toolkit,
    implements,
    IConfigurer,
    IRoutes,
    IPackageController,
    IValidators,
    ITemplateHelpers,
    SingletonPlugin
)
from ckanext.custom_schema.validators import (
    tag_not_empty
)
import ckanext.custom_schema.helpers as schema_helpers


class customSchema(SingletonPlugin):
    implements(IConfigurer)
    implements(IRoutes, inherit=True)
    implements(IPackageController, inherit=True)
    implements(IValidators)
    implements(ITemplateHelpers)

    # IConfigurer
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

    # IRoutes
    def before_map(self,m):
        m.connect(
            '/metadata_download/{package_id}',
            controller='ckanext.custom_schema.controller:CustomSchemaController',
            action='metadata_download'
        )
        return m

    # IPackageController
    def after_create(self, context, pkg_dict):
        user = context.get('user')
        group_name = pkg_dict.get('group')

        # Add dataset to "groups" based on custom field "group"
        try:
            if group_name:
                data_dict = {
                    'id': group_name,
                    'object': pkg_dict['id'],
                    'object_type': 'package',
                    'capacity': 'public'
                }
                toolkit.get_action('member_create')(context, data_dict)
        except toolkit.NotAuthorized:
            raise toolkit.ValidationError({
                'message': ['User {0} not authorized to add dataset to topic {1}'.format(user, group_name)]
            })

    def after_update(self, context, pkg_dict):
        user = context.get('user')
        group_name = pkg_dict.get('group')

        if group_name:
            existing_package = toolkit.get_action('package_show')(context, {'id': pkg_dict.get('id')})
            existing_groups = existing_package.get('groups', [])
            is_group_set = False

            # Check if group is in current groups
            for existing_group_dict in existing_groups:
                if existing_group_dict.get('name') == group_name:
                    is_group_set = True
                    break

            # Add dataset to "groups" based on custom field "group"
            if not is_group_set:
                try:
                    data_dict = {
                        'id': group_name,
                        'object': pkg_dict['id'],
                        'object_type': 'package',
                        'capacity': 'public'
                    }
                    toolkit.get_action('member_create')(context, data_dict)
                except toolkit.NotAuthorized:
                    raise toolkit.ValidationError({
                        'message': ['User {0} not authorized to add dataset to topic {1}'.format(user, group_name)]
                    })


    # IValidators
    def get_validators(self):
        return {
            'tag_not_empty': tag_not_empty
            }

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'og_get_group_list': schema_helpers.get_group_list
        }
