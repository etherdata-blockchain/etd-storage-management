from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet, basename="Category",)
router.register(r'author', views.AuthorViewSet, basename="author"),
router.register(r'location', views.LocationViewSet, basename="location"),
router.register(r'detailposition', views.DetailPositionViewSet,
                basename="detail position"),
router.register(r'itemimage', views.ItemImageViewSet, basename="Item image")
router.register(r'item', views.ItemViewSet, basename="Item")

urlpatterns = [
    path('', include(router.urls)),
    path('settings', views.GetAllSettingsViewSet.as_view()),
    path('searchByQR', views.GetByQR.as_view())
]
