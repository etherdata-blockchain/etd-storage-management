from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("storage_management/", include("storage_management.urls"),
         name="Storage_management"),
    path("api/token", TokenObtainPairView.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

