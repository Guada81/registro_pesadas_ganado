from django.urls import path
from apps.usuario.api.views import LoginView

urlpatterns = [
    path('token/', LoginView.as_view(), name='api-token-auth'),
]