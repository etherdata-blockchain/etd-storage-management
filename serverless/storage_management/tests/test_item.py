from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from ..views import CategoryViewSet, GetByQR, ItemViewSet
from ..models import MachineType, Item, DetailPosition, Owner, Location, Series
from rest_framework.test import force_authenticate
from uuid import uuid4


class TestGetItems(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="1234")
        self.factory = APIRequestFactory()
        self.category = MachineType.objects.create(name="test")
        self.author = Owner.objects.create(name="test")
        self.series = Series.objects.create(name="test series")
        self.location = Location.objects.create(country="a")
        self.position = DetailPosition.objects.create(position="test position")

    def test_list_item(self):
        Item.objects.create(name="test item",
                            detail_position=self.position,
                            location=self.location,
                            series=self.series,
                            category=self.category,
                            author=self.author)
        Item.objects.create(name="test item 2",
                            detail_position=self.position,
                            location=self.location,
                            series=self.series,
                            category=self.category,
                            author=self.author)
        request = self.factory.get('/item/')
        view = ItemViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_item(self):
        item = Item.objects.create(name="test item 2",
                                   detail_position=self.position,
                                   location=self.location,
                                   series=self.series,
                                   category=self.category,
                                   author=self.author)
        request = self.factory.get('/item/')
        view = ItemViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=item.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], item.id)

    def test_create_item_no_auth(self):
        request = self.factory.post('/item/', data={
            'name': "test",
            'author_id': self.author.id
        })
        view = ItemViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_create_item_with_auth(self):
        request = self.factory.post('/item/', data={
            'name': "test",
            'author_id': self.author.id,
            'category_id': self.category.id,
            'position_id': self.position.id,
            'location_id': self.location.id,
            'series_id': self.series.id
        })
        view = ItemViewSet.as_view({"post": "create"})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'test')
