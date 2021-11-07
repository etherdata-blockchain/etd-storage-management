# Bind device with user
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Owner, Item
from .serializers import ItemSerializer, ItemAbstractSerializer


class BindDeviceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.data.get("user")
        device = request.data.get("device")

        owner = Owner.objects.filter(user_id=user).first()
        device = Item.objects.filter(qr_code=device).first()

        if not device:
            return Response(data={"err": "Cannot find device with this device id"}, status=404)

        if not owner:
            owner = Owner.objects.create(user_id=user)

        if device.owner:
            return Response(data={"err": "This device has already been registered"}, status=500)

        device.owner = owner
        device.save()

        return Response(status=201)


class GetOwnerDevicesView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.query_params.get("user")

        print(Owner.objects.filter(user_id=user).exists())

        if not Owner.objects.filter(user_id=user).exists():
            return Response(data={"error": "User doesn't exist"}, status=404)

        devices = Item.objects.filter(owner__user_id=user)
        data = ItemAbstractSerializer(devices, many=True)
        return Response(data=data.data, status=200)
