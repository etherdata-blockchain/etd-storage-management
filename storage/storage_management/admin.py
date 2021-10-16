from django.contrib import admin
from .models import *


@admin.register(ItemImage, Location, DetailPosition, MachineType)
class Admin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_filter = ("owner", "machine_type", "status")
    search_fields = ("qr_code",)
    autocomplete_fields = ("owner",)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    search_fields = ("user_id",)