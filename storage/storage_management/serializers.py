from abc import ABC
from .models import *
from rest_framework import serializers


class ImageRelatedField(serializers.RelatedField, ABC):
    def to_representation(self, value: ItemImage):
        return value.image.url


class MachineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineType
        fields = "__all__"


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj: Location):
        return f"{str(obj)}"

    class Meta:
        model = Location
        fields = ("uuid", "country", "city", "street",
                  "building", "unit", "room_number", "name", "latitude", "longitude")


class DetailPositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj: DetailPosition):
        return f"{str(obj)}"

    class Meta:
        model = DetailPosition
        fields = ("position", "description", "name", "uuid", "image")


class ItemImageSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source="item.name")
    machine_type = MachineTypeSerializer(source="item.machine_type", read_only=True)

    class Meta:
        model = ItemImage
        fields = ("id", "image", "item", "item_name", "machine_type")


class AbstractItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ("id", "image")


class ItemSerializer(serializers.ModelSerializer):
    images = ImageRelatedField(many=True,
                               read_only=True)
    images_objects = ItemImageSerializer(source="images",
                                         many=True,
                                         read_only=True)
    owner_name = OwnerSerializer(source="owner",
                                 read_only=True)
    machine_type_name = MachineTypeSerializer(source="machine_type",
                                              read_only=True)
    location_name = LocationSerializer(source="location",
                                       read_only=True)
    position_name = DetailPositionSerializer(source="detail_position",
                                             read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(source="owner",
                                                  queryset=Owner.objects.all(), write_only=True,
                                                  required=True)
    machine_type_id = serializers.PrimaryKeyRelatedField(source="machine_type",
                                                         queryset=MachineType.objects.all(),
                                                         write_only=True,
                                                         required=True)
    location_id = serializers.PrimaryKeyRelatedField(source="location",
                                                     queryset=Location.objects.all(),
                                                     write_only=True,
                                                     required=True)
    position_id = serializers.PrimaryKeyRelatedField(source="detail_position",
                                                     queryset=DetailPosition.objects.all(),
                                                     write_only=True,
                                                     required=True)

    class Meta:
        model = Item
        fields = ("name", "description", "price", "column", "row", "qr_code", "created_time",
                  "owner_name", "machine_type_name", "location_name", "position_name",
                  "images", "owner_id", "machine_type_id", "location_id", "position_id",
                  "uuid", "images_objects")


class ItemAbstractSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source="owner.user_name")
    machine_type_name = serializers.ReadOnlyField(source="machineType.name")
    position = serializers.ReadOnlyField(source="detail_position.position")

    # images = AbstractItemImageSerializer(many=True,
    #                                      read_only=True)

    class Meta:
        model = Item
        fields = ("uuid", "name", "description",
                  "owner_name", "machine_type_name",
                  "column", "row",
                  "position", "images", "price", "qr_code")


class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = ("items", "group_name", "creation_time")
