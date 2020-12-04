import ckan.lib.search
from ckantoolkit.tests import helpers, factories

from ckanext.custom_schema.helpers import (
    get_group_list,
    get_selected_group
)


class TestGetGroupList(object):
    @classmethod
    def setup(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    @classmethod
    def teardown(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    def test_group_list_no_results(self):
        assert (
            get_group_list() == []
        )

    def test_group_list_with_results(self):
        group1 = factories.Group(name='water')
        group2 = factories.Group(name='transportation')
        group3 = factories.Group(name='economy')
        group_from_helpers = get_group_list()
        assert (
            group_from_helpers[0]['name'] == 'economy'
        )
        assert (
            group_from_helpers[1]['name'] == 'transportation'
        )
        assert (
            group_from_helpers[2]['name'] == 'water'
        )


class TestGetSelectedGroup(object):
    @classmethod
    def setup(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    @classmethod
    def teardown(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    def test_selected_group_with_no_groups(self):
        dataset = factories.Dataset(
            tag_string='geography',
            accessLevel='public',
            contact_name='John Smith',
            contact_email='jsmith@test.com',
            rights='No restrictions on public use',
            accrualPeriodicity='R/P1W'
        )
        assert (
            get_selected_group(dataset) == ''
        )

    def test_selected_group_with_several_groups(self):
        group1 = factories.Group(name='economy')
        group2 = factories.Group(name='transportation')
        group3 = factories.Group(name='water')
        dataset = factories.Dataset(
            tag_string='geography',
            accessLevel='public',
            contact_name='John Smith',
            contact_email='jsmith@test.com',
            rights='No restrictions on public use',
            accrualPeriodicity='R/P1W',
            groups=[
                {'name': group2['name']},
                {'name': group3['name']}
            ]
        )
        assert (
            get_selected_group(dataset) == 'transportation'
        )
