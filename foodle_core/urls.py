from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SaasTenantListCreateView, StaffUserViewSet

router = DefaultRouter()
router.register('users', StaffUserViewSet, basename='staff-user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/saas/tenants/', SaasTenantListCreateView.as_view()),
    path('api/', include(router.urls)),
    path('api/finance/', include('finance.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/billing/', include('billing.urls')),
]
