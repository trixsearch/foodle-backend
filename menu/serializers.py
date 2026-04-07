from rest_framework import serializers

from finance.models import TaxSlab
from finance.serializers import TaxSlabSerializer

from .models import AddOn, MenuCategory, MenuItem, MenuVariation


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = (
            'id',
            'name',
            'food_type',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class MenuVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVariation
        fields = (
            'id',
            'menu_item',
            'name',
            'price_adjustment',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class MenuItemSerializer(serializers.ModelSerializer):
    category_detail = MenuCategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.all(),
        write_only=True,
    )
    tax_slab_detail = TaxSlabSerializer(source='tax_slab', read_only=True)
    tax_slab = serializers.PrimaryKeyRelatedField(
        queryset=TaxSlab.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = MenuItem
        fields = (
            'id',
            'name',
            'category',
            'category_detail',
            'base_price',
            'tax_slab',
            'tax_slab_detail',
            'short_code',
            'is_active',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'category_detail',
            'tax_slab_detail',
            'created_at',
            'updated_at',
        )


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = (
            'id',
            'name',
            'price',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
