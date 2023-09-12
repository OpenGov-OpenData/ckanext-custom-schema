from flask import Blueprint, make_response

import ckanext.custom_schema.cademo.utils as utils

cademo_schema = Blueprint('cademo_schema', __name__)


def metadata_download(package_id):
    response = make_response()
    response.headers[u'content-type'] = u'application/octet-stream'
    return utils.metadata_download(package_id, response)


cademo_schema.add_url_rule(
    '/metadata_download/<package_id>',
    view_func=metadata_download
)


def get_blueprints():
    return [cademo_schema]
