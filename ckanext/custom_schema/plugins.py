from ckan.plugins import toolkit, IConfigurer, IRoutes, SingletonPlugin, implements

class customSchema(SingletonPlugin):
    implements(IConfigurer)
    implements(IRoutes,inherit=True)

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

