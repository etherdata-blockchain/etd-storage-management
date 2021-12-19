from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from ..views import MachineTypeViewSet, GetByQR
from ..models import MachineType, Item, DetailPosition
from rest_framework.test import force_authenticate
from uuid import uuid4


class TestGetItems(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test", password="1234")

        category = MachineType(name="abc")
        category.save()

        self.ud = uuid4()
        self.ud2 = uuid4()
        self.ud3 = uuid4()

        position = DetailPosition(uuid=self.ud3)
        position.save()
        item = Item(name="abc", uuid=self.ud)
        item2 = Item(name="cde", qr_code=self.ud2)
        item3 = Item(name="efg", detail_position=position, qr_code=uuid4())
        item4 = Item(name="hij", detail_position=position, qr_code=uuid4())

        item.save()
        item2.save()
        item3.save()
        item4.save()

    def test_get_category(self):
        factory = APIRequestFactory()
        request = factory.get("/category/")
        force_authenticate(request, user=self.user)
        view = MachineTypeViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "abc")

    def test_create_category(self):
        factory = APIRequestFactory()
        request = factory.post("/category/", {"name": "cde"})
        force_authenticate(request, user=self.user)
        view = MachineTypeViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "cde")

    def test_search_by_qr(self):
        """
        By uuid
        :return:
        """
        factory = APIRequestFactory()
        request = factory.get("/searchByQR/", {"qr": self.ud})
        force_authenticate(request, user=self.user)
        view = GetByQR.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200, response)
        self.assertEqual(response.data['name'], "abc")

    def test_search_by_qr2(self):
        """
        By qr
        :return:
        """
        factory = APIRequestFactory()
        request = factory.get("/searchByQR/", {"qr": self.ud2})
        force_authenticate(request, user=self.user)
        view = GetByQR.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200, response)
        self.assertEqual(response.data['name'], "cde")

    def test_search_by_qr3(self):
        """
        By qr
        :return:
        """
        factory = APIRequestFactory()
        request = factory.get("/searchByQR/", {"qr": self.ud3})
        force_authenticate(request, user=self.user)
        view = GetByQR.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200, response)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], "efg")
        self.assertEqual(response.data[1]['name'], "hij")
