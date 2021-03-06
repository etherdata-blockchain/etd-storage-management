from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from .filters.item_filter import ItemFilter
from .paginator import TotalPagePagination
from .serializers import *
from .models import *
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class GetByQR(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemAbstractSerializer()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        data = Item.objects.filter(qr_code=request.query_params['qr']).first()
        if data:
            print("Get item By qr")
            return Response(ItemAbstractSerializer(data).data)

        try:

            data = Item.objects.filter(
                Q(uuid=request.query_params['qr'])).first()
            if data:
                print("Get item By uuid")
                return Response(ItemAbstractSerializer(data).data)

            p = DetailPosition.objects.filter(
                uuid=request.query_params['qr']).first()
            if p:
                print("Get item by position")
                items = Item.objects.filter(detail_position=p)
                print(items)
                if items:
                    data = ItemAbstractSerializer(items, many=True)
                    return Response(data=data.data, status=200)

            return Response(data=[], status=404)
        except Exception as e:
            return Response(data=[], status=404)


class MachineTypeViewSet(viewsets.ModelViewSet):
    queryset = MachineType.objects.all()
    serializer_class = MachineTypeSerializer
    permission_classes = [IsAuthenticated]


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("user_id")
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TotalPagePagination


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]


class DetailPositionViewSet(viewsets.ModelViewSet):
    queryset = DetailPosition.objects.all()
    serializer_class = DetailPositionSerializer
    permission_classes = [IsAuthenticated]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('qr_code')
    serializer_class = ItemSerializer
    pagination_class = TotalPagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ItemFilter
    permission_classes = [IsAuthenticated]
    search_fields = ['qr_code']


class ItemImageViewSet(viewsets.ModelViewSet):
    queryset = ItemImage.objects.all()
    serializer_class = ItemImageSerializer
    permission_classes = [IsAuthenticated]


class GetItemByLocationView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        pid = request.query_params['position_id']
        items = Item.objects.filter(detail_position=pid)
        print(items)
        if items:
            data = ItemSerializer(items, many=True)
            return Response(data=data.data, status=200)

        return Response(data=[], status=400)


class ItemGroupViewSet(viewsets.ModelViewSet):
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
