from ckan.plugins import (
    toolkit,
    IConfigurer,
    ITemplateHelpers,
    SingletonPlugin,
    implements,
)

from ckanext.custom_schema import helpers as schema_helpers


class customSchema(SingletonPlugin):
    implements(IConfigurer)
    implements(ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_public_directory(config, "static")
        toolkit.add_template_directory(config, "templates")

        config['scheming.presets'] = """
ckanext.scheming:presets.json
"""

        config['scheming.dataset_schemas'] = """
ckanext.custom_schema:sanjose/schemas/dataset.yaml
"""

    # ITemplateHelpers
    def get_helpers(self):
        return schema_helpers.get_shared_template_helpers()
