import ckan.logic as logic
from ckan.common import c

def scheming_get_user_dict():
    context = None
    data_dict = {'id': c.user}
    user_dict = logic.get_action('user_show')(context, data_dict)
    return user_dict
