from djongo import models
from django.utils.translation import gettext as _
import uuid
from os import path
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files import File


def upload_location(instance, filename):
    filebase, extension = path.splitext(filename)
    now = datetime.now()
    return f'item-images/{now.year}/{now.month}/{now.day}/' + f"{uuid.uuid4()}{extension}"


def compress(image):
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=80)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


# Machine Type
class MachineType(models.Model):
    name = models.CharField(max_length=128, default="Raspberry Pi", unique=True)
    hashRate = models.FloatField(default=0, help_text="Machine's base hash rate")
    disk_storage = models.FloatField(default=0, help_text="Storage in MB.")
    memory_size = models.FloatField(default=0, help_text="Size in MB")
    os_version = models.CharField(default="Ubuntu 20.04", max_length=128)

    def __str__(self):
        return f"{self.name} - {self.disk_storage}MB"


class Owner(models.Model):
    user_name = models.CharField(null=True, blank=True, max_length=128)
    user_id = models.CharField(max_length=128, default="", unique=True)
    coinbase = models.TextField(default="No content here", null=True, blank=True, help_text="User's coinbase")

    def __str__(self):
        return f"{self.user_id} {self.user_name}"


# Address
class Location(models.Model):
    country = models.CharField(max_length=128, default="China")
    city = models.CharField(max_length=128, default="Shenzhen")
    street = models.CharField(
        max_length=128, default="Some Street", null=True, blank=True)
    building = models.CharField(
        max_length=128, default="Some Building", null=True, blank=True)
    unit = models.CharField(
        max_length=128, default="Some Unit", null=True, blank=True)
    room_number = models.CharField(max_length=128, default="Some RM Number")

    latitude = models.FloatField(null=True, blank=True)

    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.country}{self.city}{self.building}"


class DetailPosition(models.Model):
    position = models.CharField(max_length=1024, default="Book Shelf 1")
    description = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # call the compress function
        if self.image:
            try:
                new_image = compress(self.image)
                # set self.image to new_image
                self.image = new_image
            except Exception as e:
                pass
        # save
        super().save(*args, **kwargs)

    def __str__(self):
        return self.position


class Item(models.Model):
    STORAGE_STATS = [("pending", "Pending"), ("installed", "Installed"), ("delivered", "Delivered"), ("out", "Out"),
                     ("error", "Error")]

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=1024, default="", verbose_name=_("Item Name"),
                            help_text="Please Enter your item name")
    description = models.TextField(blank=True, null=True,
                                   help_text="Please enter your item description")
    owner = models.ForeignKey(
        Owner, on_delete=models.SET_NULL, blank=True, null=True)
    created_time = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    machine_type = models.ForeignKey(
        MachineType, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField(default=0.0)
    qr_code = models.CharField(max_length=10008, primary_key=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True)
    detail_position = models.ForeignKey(DetailPosition, on_delete=models.SET_NULL, blank=True, null=True
                                        )
    status = models.CharField(default="pending", choices=STORAGE_STATS, help_text="Current storage status",
                              max_length=128)
    column = models.IntegerField(default=1)
    row = models.IntegerField(default=1)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    title = models.CharField(
        max_length=128, default="Face", null=True, blank=True)
    image = models.ImageField(verbose_name=_(
        "Item Image"), upload_to=upload_location)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="images")

    def save(self, *args, **kwargs):
        # call the compress function
        if self.image:
            try:
                new_image = compress(self.image)
                # set self.image to new_image
                self.image = new_image
            except Exception as e:
                pass
        # save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image-{self.item.name.title()}"


class ItemGroup(models.Model):
    items = models.ArrayReferenceField(
        to=Item,
        on_delete=models.CASCADE,
        blank=True,
        null=True,

    )
    group_name = models.CharField(help_text="Enter the group name", max_length=64, primary_key=True)
    creation_time = models.DateTimeField(auto_now_add=True)
