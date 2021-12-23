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
from ckanext.custom_schema.cademo.validators import (
    tag_not_empty
)
import ckanext.custom_schema.cademo.helpers as schema_helpers


get_action = toolkit.get_action


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
ckanext.custom_schema:cademo/schemas/presets.yaml
"""

        config['scheming.dataset_schemas'] = """
ckanext.custom_schema:cademo/schemas/dataset.yaml
"""

    # IRoutes
    def before_map(self,m):
        m.connect(
            '/metadata_download/{package_id}',
            controller='ckanext.custom_schema.cademo.controller:CustomSchemaController',
            action='metadata_download'
        )
        return m

    # IPackageController
    def after_create(self, context, pkg_dict):
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
                get_action('member_create')(context, data_dict)
        except toolkit.NotAuthorized:
            raise toolkit.ValidationError({
                'message': [
                    'User "{0}" not authorized to add dataset to topic {1}'.format(
                        context.get('user'), group_name
                    )
                ]
            })

    def after_update(self, context, pkg_dict):
        group_name = pkg_dict.get('group')

        if group_name:
            existing_package = get_action('package_show')(context, {'id': pkg_dict.get('id')})
            existing_groups = existing_package.get('groups', [])
            existing_group_names = [item.get('name') for item in existing_groups]

            # Add dataset to "groups" if not in any existing groups
            if group_name not in existing_group_names:
                try:
                    data_dict = {
                        'id': group_name,
                        'object': pkg_dict['id'],
                        'object_type': 'package',
                        'capacity': 'public'
                    }
                    get_action('member_create')(context, data_dict)
                except toolkit.NotAuthorized:
                    raise toolkit.ValidationError({
                        'message': [
                            'User "{0}" not authorized to add dataset to topic {1}'.format(
                                context.get('user'), group_name
                            )
                        ]
                    })

                # Remove dataset from other groups
                try:
                    for group_dict in existing_groups:
                        if group_name != group_dict.get('name'):
                            data_deletion_dict = {
                                'id': group_dict['id'],
                                'object': pkg_dict['id'],
                                'object_type': 'package'
                            }
                            get_action('member_delete')(context, data_deletion_dict)
                except toolkit.NotAuthorized:
                    raise toolkit.ValidationError({
                        'message': [
                            'User "{0}" not authorized to remove dataset from topic {1}'.format(
                                context.get('user'), group_dict.get('name')
                            )
                        ]
                    })


    # IValidators
    def get_validators(self):
        return {
            'tag_not_empty': tag_not_empty
        }


    # ITemplateHelpers
    def get_helpers(self):
        return {
            'og_get_group_list': schema_helpers.get_group_list,
            'og_get_selected_group': schema_helpers.get_selected_group
        }
