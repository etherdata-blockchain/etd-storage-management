from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from ..models import Owner, Item, MachineType, Location, DetailPosition
from ..util_views import BindDeviceView, GetOwnerDevicesView


class TestBind(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username="test", password="1234")
        self.machine_type = MachineType.objects.create(name="test")
        self.location = Location.objects.create(country="a")
        self.position = DetailPosition.objects.create(position="test position")
        Item.objects.create(name="Test Object", machine_type=self.machine_type, location=self.location,
                            detail_position=self.position, qr_code="test_device")

    def test_bind_device(self):
        Owner.objects.create(user_id="abcde")
        factory = APIRequestFactory()
        request = factory.post("/bind/", data={"user": "abcde", "device": "test_device"})
        force_authenticate(request, user=self.user)
        view = BindDeviceView.as_view()
        response = view(request)

        item = Item.objects.get(name="Test Object")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(item.owner.user_id, "abcde")

    def test_bind_device_user_not_exists(self):
        factory = APIRequestFactory()
        request = factory.post("/bind/", data={"user": "abcde", "device": "test_device"})
        force_authenticate(request, user=self.user)
        view = BindDeviceView.as_view()
        response = view(request)

        item = Item.objects.get(name="Test Object")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Owner.objects.count(), 1)
        self.assertEqual(item.owner.user_id, "abcde")

    def test_bind_device_and_both_not_exist(self):
        factory = APIRequestFactory()
        request = factory.post("/bind/", data={"user": "abc", "device": "test"})
        force_authenticate(request, user=self.user)
        view = BindDeviceView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Owner.objects.count(), 0)

    def test_bind_device_with_owner(self):
        owner =  Owner.objects.create(user_id="my_owner")
        Item.objects.create(name="Test Object", machine_type=self.machine_type, location=self.location,
                            detail_position=self.position, qr_code="test_test", owner=owner)
        factory = APIRequestFactory()
        request = factory.post("/bind/", data={"user": "my_owner", "device": "test_test"})
        force_authenticate(request, user=self.user)
        view = BindDeviceView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 500)



class TestGetUserDevices(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test", password="1234")
        self.machine_type = MachineType.objects.create(name="test")
        self.location = Location.objects.create(country="a")
        self.owner = Owner.objects.create(user_id="test")
        self.position = DetailPosition.objects.create(position="test position")
        Item.objects.create(name="Test Object", machine_type=self.machine_type, location=self.location,
                            detail_position=self.position, qr_code="test_device", owner=self.owner)

    def test_get_user_devices(self):
        factory = APIRequestFactory()
        request = factory.get("?user=test")
        force_authenticate(request, user=self.user)
        view = GetOwnerDevicesView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
