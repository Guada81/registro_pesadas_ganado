from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.animal.api.views import AnimalViewSet

router = DefaultRouter()
router.register(r'animales', AnimalViewSet, basename='animal-api')

urlpatterns = [
    path('', include(router.urls)),
]