from ckan.lib.base import BaseController
from ckan.common import response
import ckanext.custom_schema.cademo.utils as utils


class CustomSchemaController(BaseController):
    def metadata_download(self, package_id):
        return utils.metadata_download(package_id, response)
