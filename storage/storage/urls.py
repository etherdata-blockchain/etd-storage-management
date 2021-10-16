from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include("webapp.urls")),
    path('admin/', admin.site.urls),
    path("storage_management/", include("storage_management.urls"),
         name="Storage_management")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

