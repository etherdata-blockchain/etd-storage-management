from django.contrib import admin
from .models import *


@admin.register(Owner, ItemImage, Item, Location, DetailPosition, MachineType)
class GlacierAdmin(admin.ModelAdmin):
    pass
