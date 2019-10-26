from six import string_types

from ckan.plugins.toolkit import missing, _, get_validator

from ckanext.scheming.validation import scheming_validator

ignore_missing = get_validator('ignore_missing')
not_empty = get_validator('not_empty')


@scheming_validator
def tag_not_empty(field, schema):
    def validator(key, data, errors, context):
        # get list of tags from tag_string
        if isinstance(data[key], string_types):
            tags = [tag.strip() \
                    for tag in data[key].split(',') \
                    if tag.strip()]
        else:
            tags = data[key]

        # ignore missing tag_string if tags is present
        if tags is missing or not tags:
            package = context.get('package')
            if package:
                model = context['model']
                session = context['session']
                pkg = session.query(model.Package).get(package.id)
                pkg_tags = pkg.get_tags()
                if pkg_tags:
                    return ignore_missing(key, data, errors, context)

        return not_empty(key, data, errors, context)

    return validator
