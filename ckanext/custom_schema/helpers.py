import ckan.plugins as p

get_action = p.toolkit.get_action
ValidationError = p.toolkit.ValidationError

def get_group_list():
    try:
        data_dict_global_results = {
            'all_fields': True,
            'sort': 'title asc',
            'type': 'group',
        }
        global_results = get_action('group_list')({}, data_dict_global_results)
        return global_results
    except ValidationError:
        return []
