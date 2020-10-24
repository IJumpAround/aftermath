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

    def test_quantity_on_items(self):
        response = self.client.get('/items/')

        items = response.json().get('resources').get('data')

        for item in items:
            self.assertIsNotNone(item.get('quantity'))

    def test_can_resolve_pks(self):
        response = self.client.get('/items/')

        items = response.json().get('resources').get('data')

        for item in items:
            slug = f'/{item.get("model_type")}/'
            print(resolve(f'/{item.get("model_type")}/'))

    def test_pagination_limit_page(self):
        page = 1
        limit = 2
        print (resolve('/items/'))
        # url = resolve('/items/', kwargs={'page': page, 'limit':limit})
        resources = self.client.get('/items/',{'page': page, 'limit':limit} ).json().get('resources')

        self.assertEqual(len(resources.get('data')), limit)
        self.assertEqual(resources.get('next_page'), 2)

    def test_pagination_order(self):
        order = '-player'

        resources = self.client.get('/items/', {'order_by':order}).json().get('resources')
        items = resources.get('data')

        s = sorted(items, key=lambda i: i['player'])

        for i in range(len(s)):
            self.assertEqual(s[i]['player'], items[i]['player'])
        print(resources)

    def test_default_pagination_order_uses_name(self):

        resources = self.client.get('/items/').json().get('resources')
        items = resources.get('data')

        s = sorted(items, key=lambda i: i['name'])

        for i in range(len(s)):
            self.assertEqual(s[i]['player'], items[i]['player'])