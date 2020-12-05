import ckan.lib.search
from ckantoolkit.tests import helpers, factories
from ckan.plugins.toolkit import ValidationError

import nose.tools

assert_raises = nose.tools.assert_raises


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


class TestUserAuthWithGroupModifier(object):
    @classmethod
    def setup(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    @classmethod
    def teardown(self):
        helpers.reset_db()
        ckan.lib.search.clear_all()

    def test_package_create_without_group_permission(self):
        user = factories.User(name='user1')
        owner_org = factories.Organization(
            users=[
                {'name': user['name'], 'capacity': 'editor'}
            ]
        )
        group = factories.Group(name='economy')

        context = {'user': user['name'], 'ignore_auth': False}
        params = {
            'name': 'test-dataset-1',
            'notes': 'This is a test',
            'tag_string': 'geography',
            'accessLevel': 'public',
            'contact_name': 'John Smith',
            'contact_email': 'jsmith@test.com',
            'rights': 'No restrictions on public use',
            'accrualPeriodicity': 'R/P1W',
            'owner_org': owner_org['id'],
            'group': 'economy'
        }

        assert_raises(
            ValidationError,
            helpers.call_action, 'package_create', context, **params
        )

    def test_package_create_with_group_permission(self):
        user = factories.User(name='user2')
        owner_org = factories.Organization(
            users=[
                {'name': user['name'], 'capacity': 'editor'}
            ]
        )
        group = factories.Group(
            name='economy',
            users=[
                {'name': user['name'], 'capacity': 'member'}
            ]
        )

        context = {'user': user['name'], 'ignore_auth': False}
        params = {
            'name': 'test-dataset-2',
            'notes': 'This is a test',
            'tag_string': 'geography',
            'accessLevel': 'public',
            'contact_name': 'John Smith',
            'contact_email': 'jsmith@test.com',
            'rights': 'No restrictions on public use',
            'accrualPeriodicity': 'R/P1W',
            'owner_org': owner_org['id'],
            'group': 'economy'
        }
        dataset = helpers.call_action(
            'package_create',
            context=context,
            **params
        )

        assert dataset['groups'][0]['name'] == 'economy'

    def test_package_patch_with_group_permission(self):
        user = factories.User(name='user3')
        owner_org = factories.Organization(
            users=[
                {'name': user['name'], 'capacity': 'editor'}
            ]
        )
        group1 = factories.Group(
            name='economy',
            users=[
                {'name': user['name'], 'capacity': 'member'}
            ]
        )
        group2 = factories.Group(
            name='transportation',
            users=[
                {'name': user['name'], 'capacity': 'member'}
            ]
        )

        context = {'user': user['name'], 'ignore_auth': False}
        create_params = {
            'name': 'test-dataset-3',
            'notes': 'This is a test',
            'tag_string': 'geography',
            'accessLevel': 'public',
            'contact_name': 'John Smith',
            'contact_email': 'jsmith@test.com',
            'rights': 'No restrictions on public use',
            'accrualPeriodicity': 'R/P1W',
            'owner_org': owner_org['id'],
            'group': 'economy'
        }
        dataset = helpers.call_action(
            'package_create',
            context=context,
            **create_params
        )

        patch_params = {
            'id': 'test-dataset-3',
            'group': 'transportation'
        }
        dataset = helpers.call_action(
            'package_patch',
            context=context,
            **patch_params
        )
        assert dataset['groups'][0]['name'] == 'transportation'
