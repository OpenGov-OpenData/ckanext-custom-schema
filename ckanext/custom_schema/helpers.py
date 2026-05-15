"""Shared Jinja / ITemplateHelpers utilities for custom_schema plugins."""

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


def get_selected_group(data):
    try:
        group_list = data.get('groups', [])
        for item in group_list:
            if item.get('name'):
                return item.get('name')
    except (TypeError, ValueError):
        pass
    return ''


def is_data_dict_active(ddict):
    """Return True if data dictionary is populated (label or notes on any column)."""
    for col in ddict:
        info = col.get('info', {})
        if info.get('label') or info.get('notes'):
            return True
    return False


def get_shared_template_helpers():
    """Return the helper name -> callable mapping for ITemplateHelpers.get_helpers."""
    return {
        'og_get_group_list': get_group_list,
        'og_get_selected_group': get_selected_group,
        'og_is_data_dict_active': is_data_dict_active,
    }
