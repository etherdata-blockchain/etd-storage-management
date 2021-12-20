import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from ..views import MachineTypeViewSet, GetByQR, ItemViewSet
from ..models import MachineType, Item, DetailPosition, Owner, Location
from rest_framework.test import force_authenticate
from uuid import uuid4


class TestGetItems(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="1234")
        self.factory = APIRequestFactory()
        self.owner = Owner.objects.create(user_name="test", user_id="1")
        self.machine_type = MachineType.objects.create(name="test")
        self.location = Location.objects.create(country="a", uuid=uuid.uuid4())
        self.position = DetailPosition.objects.create(position="test position")

    def test_list_item(self):
        Item.objects.create(name="test item",
                            detail_position=self.position,
                            location=self.location,
                            machine_type=self.machine_type,
                            owner=self.owner,
                            qr_code="1")
        Item.objects.create(name="test item 2",
                            detail_position=self.position,
                            location=self.location,
                            machine_type=self.machine_type,
                            owner=self.owner,
                            qr_code="2")
        request = self.factory.get('/item/')
        force_authenticate(request, user=self.user)
        view = ItemViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_item(self):
        item = Item.objects.create(name="test item 2",
                                   detail_position=self.position,
                                   location=self.location,
                                   machine_type=self.machine_type,
                                   owner=self.owner)
        request = self.factory.get('/item/')
        force_authenticate(request, user=self.user)
        view = ItemViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=item.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['qr_code'], str(item.qr_code))

    def test_create_item_no_auth(self):
        request = self.factory.post('/item/', data={
            'name': "test",
            'owner_id': self.owner.pk
        })
        view = ItemViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, 401)

    def test_create_item_with_auth(self):
        request = self.factory.post('/item/', data={
            'name': "test",
            'owner_id': self.owner.pk,
            'machine_type_id': self.machine_type.pk,
            'position_id': self.position.pk,
            'location_id': self.location.pk,
            "qr_code": "1"
        })
        force_authenticate(request, user=self.user)
        view = ItemViewSet.as_view({"post": "create"})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'test')
