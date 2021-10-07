from django.urls import include, path
from rest_framework import routers
from . import views
from . import util_views

router = routers.DefaultRouter()
router.register(r'machine_type', views.MachineTypeViewSet, basename="machine_type", )
router.register(r'owner', views.OwnerViewSet, basename="owner"),
router.register(r'location', views.LocationViewSet, basename="location"),
router.register(r'detailposition', views.DetailPositionViewSet,
                basename="detail position"),
router.register(r'itemimage', views.ItemImageViewSet, basename="Item image")
router.register(r'item', views.ItemViewSet, basename="Item")

urlpatterns = [
    path('', include(router.urls)),
    path('settings', views.GetAllSettingsViewSet.as_view()),
    path('searchByQR', views.GetByQR.as_view()),
    path('device', util_views.GetOwnerDevicesView.as_view()),
    path("device/register", util_views.BindDeviceView.as_view())
]
