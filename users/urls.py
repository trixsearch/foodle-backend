from django.urls import path

from .views import CurrentTenantAPIView, LoginAPIView, MeAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='auth-login'),
    path('me/', MeAPIView.as_view(), name='auth-me'),
    path('tenant/', CurrentTenantAPIView.as_view(), name='auth-tenant'),
]
