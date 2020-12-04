import ckan.lib.search
from ckantoolkit.tests import helpers, factories


class TestPackageWithGroupModifier(object):
    @classmethod
    def setup(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    @classmethod
    def teardown(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    def test_package_create_without_any_group_modifier(self):
        dataset = factories.Dataset(
            name='test-dataset-1',
            tag_string='geography',
            accessLevel='public',
            contact_name='John Smith',
            contact_email='jsmith@test.com',
            rights='No restrictions on public use',
            accrualPeriodicity='R/P1W'
        )

        assert dataset['groups'] == []

    def test_package_create_with_group_modifier(self):
        group1 = factories.Group(name='economy')
        dataset = factories.Dataset(
            name='test-dataset-2',
            tag_string='geography',
            accessLevel='public',
            contact_name='John Smith',
            contact_email='jsmith@test.com',
            rights='No restrictions on public use',
            accrualPeriodicity='R/P1W',
            group='economy'
        )

        assert dataset['groups'][0]['name'] == 'economy'

    def test_package_patch_with_group_modifier(self):
        group1 = factories.Group(name='economy')
        group2 = factories.Group(name='transportation')
        group3 = factories.Group(name='water')
        dataset = factories.Dataset(
            name='test-dataset-3',
            tag_string='geography',
            accessLevel='public',
            contact_name='John Smith',
            contact_email='jsmith@test.com',
            rights='No restrictions on public use',
            accrualPeriodicity='R/P1W',
            group='economy'
        )

        assert dataset['groups'][0]['name'] == 'economy'

        dataset = helpers.call_action(
            'package_patch',
            id='test-dataset-3',
            group='transportation'
        )

        assert dataset['groups'][0]['name'] == 'transportation'
        assert len(dataset['groups']) == 1
