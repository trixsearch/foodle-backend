from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/finance/', include('finance.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/billing/', include('billing.urls')),
]
