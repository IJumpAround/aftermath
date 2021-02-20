from django.test import TestCase
from django.urls import reverse, resolve
import pprint

from item_management.test_item_management.test_data.items import add_test_data_to_class


class ItemsViewTestClass(TestCase):

    def setUp(self):
        self.item_url = '/items'
        add_test_data_to_class(self)

    def test_get_request_to_items(self):
        url = reverse('item_management:items')
        response = self.client.get(url)

        resources = response.json().get('resources').get('data')
        print(resources)
        pprint.pprint(resources)

    def test_post_request_to_items(self):
        url = reverse('item_management:items')
        response = self.client.post(url)

        resources = response.json().get('resources').get('data')
        print(resources)
        pprint.pprint(resources)

    def test_quantity_on_items(self):
        response = self.client.post('/items/')

        items = response.json().get('resources').get('data')

        for item in items:
            self.assertIsNotNone(item.get('quantity'))

    def test_can_resolve_pks(self):
        response = self.client.post('/items/')

        items = response.json().get('resources').get('data')

        for item in items:
            slug = f'/{item.get("model_type")}/'
            print(resolve(f'/{item.get("model_type")}/'))

    def test_pagination_limit_page(self):
        start = 1
        length = 2

        resources = self.client.post('/items/', {'start': start, 'length': length}).json().get('resources')

        self.assertEqual(len(resources.get('data')), length)
        self.assertEqual(resources.get('next_page'), 2)

    def test_pagination_order(self):

        request_body = {'draw': 2, 'columns': [
            {'data': 'id', 'name': '', 'searchable': True, 'orderable': True, 'search': {'value': '', 'regex': False}},
            {'data': 'model_type', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'name', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'text_description', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'rarity', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'wondrous', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'requires_attunement', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'player', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'quantity', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}},
            {'data': 'model_name', 'name': '', 'searchable': True, 'orderable': True,
             'search': {'value': '', 'regex': False}}], 'order': [{'column': 7, 'dir': 'desc'}], 'start': 0,
                        'length': 10, 'search': {'value': '', 'regex': False}}

        resources = self.client.post('/items/', data=request_body, content_type='application/json').json().get('resources')
        items = resources.get('data')

        s = sorted(items, key=lambda i: i['player'])

        for i in range(len(s)):
            self.assertEqual(s[i]['player'], items[i]['player'])
        print(resources)

    def test_default_pagination_order_uses_name(self):

        resources = self.client.post('/items/').json().get('resources')
        items = resources.get('data')

        s = sorted(items, key=lambda i: i['name'])

        for i in range(len(s)):
            self.assertEqual(s[i]['player'], items[i]['player'])
