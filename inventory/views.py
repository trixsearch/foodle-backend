from rest_framework import viewsets

from .models import RawMaterial, Recipe, RecipeIngredient
from .serializers import RawMaterialSerializer, RecipeIngredientSerializer, RecipeSerializer


class RawMaterialViewSet(viewsets.ModelViewSet):
    queryset = RawMaterial.objects.all()
    serializer_class = RawMaterialSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('menu_item', 'menu_item__category', 'menu_item__tax_slab').all()
    serializer_class = RecipeSerializer


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.select_related('recipe', 'raw_material').all()
    serializer_class = RecipeIngredientSerializer
