from rest_framework import viewsets

from .models import AddOn, MenuCategory, MenuItem, MenuVariation
from .serializers import (
    AddOnSerializer,
    MenuCategorySerializer,
    MenuItemSerializer,
    MenuVariationSerializer,
)


class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.select_related('category', 'tax_slab').all()
    serializer_class = MenuItemSerializer


class MenuVariationViewSet(viewsets.ModelViewSet):
    queryset = MenuVariation.objects.select_related('menu_item').all()
    serializer_class = MenuVariationSerializer


class AddOnViewSet(viewsets.ModelViewSet):
    queryset = AddOn.objects.all()
    serializer_class = AddOnSerializer
