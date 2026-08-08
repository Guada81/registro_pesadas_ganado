from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.pesada.api.views import PesadaViewSet

router = DefaultRouter()
router.register(r'pesadas', PesadaViewSet, basename='pesada-api')

urlpatterns = [
    path('', include(router.urls)),
]