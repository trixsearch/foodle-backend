from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddOnViewSet,
    MenuCategoryViewSet,
    MenuItemViewSet,
    MenuVariationViewSet,
)

router = DefaultRouter()
router.register(r'categories', MenuCategoryViewSet, basename='menucategory')
router.register(r'items', MenuItemViewSet, basename='menuitem')
router.register(r'variations', MenuVariationViewSet, basename='menuvariation')
router.register(r'add-ons', AddOnViewSet, basename='addon')

urlpatterns = [
    path('', include(router.urls)),
]
