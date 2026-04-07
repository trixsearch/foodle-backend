from rest_framework import serializers

from menu.models import MenuItem
from menu.serializers import MenuItemSerializer

from .models import RawMaterial, Recipe, RecipeIngredient


class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterial
        fields = (
            'id',
            'name',
            'unit_of_measurement',
            'current_stock',
            'minimum_stock_alert',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'recipe',
            'raw_material',
            'quantity_required',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class RecipeSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'menu_item',
            'menu_item_detail',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'menu_item_detail', 'created_at', 'updated_at')
