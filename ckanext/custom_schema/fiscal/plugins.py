import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
from ckanext.custom_schema.fiscal import helpers

class customSchema(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_public_directory(config, "static")
        toolkit.add_template_directory(config, "templates")       
 
        config['scheming.presets'] = """
ckanext.custom_schema:fiscal/schemas/presets.yaml
"""

        config['scheming.dataset_schemas'] = """
ckanext.custom_schema:fiscal/schemas/dataset.yaml
"""

    def get_helpers(self):
        return {
            'scheming_get_user_dict': helpers.scheming_get_user_dict,
            }
