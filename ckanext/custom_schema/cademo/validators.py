from six import string_types

from ckan.plugins.toolkit import missing, _, get_validator

from ckanext.scheming.validation import scheming_validator

ignore_missing = get_validator('ignore_missing')
not_empty = get_validator('not_empty')


@scheming_validator
def tag_not_empty(field, schema):
    # Default validator for tag_string is not_empty
    # If tag_string is empty set it to current package tags
    def validator(key, data, errors, context):
        # get list of tags from tag_string
        if isinstance(data[key], string_types):
            tags = [tag.strip() \
                    for tag in data[key].split(',') \
                    if tag.strip()]
        else:
            tags = data[key]

        # check if tag_string is missing or empty
        if tags is missing or not tags:
            package = context.get('package')
            # check if there's a package
            if package:
                model = context['model']
                session = context['session']
                pkg = session.query(model.Package).get(package.id)
                pkg_tags = pkg.get_tags()
                # check if package has tags and adds them to tag_string
                if pkg_tags:
                    tag_list = [t.name for t in pkg_tags]
                    data[key] = ",".join(tag_list)
                    return ignore_missing(key, data, errors, context)

        return not_empty(key, data, errors, context)

    return validator
