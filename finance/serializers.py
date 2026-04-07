from rest_framework import serializers

from .models import DiscountConfig, TaxSlab


class TaxSlabSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxSlab
        fields = (
            'id',
            'name',
            'percentage',
            'is_active',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class DiscountConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountConfig
        fields = (
            'id',
            'name',
            'discount_type',
            'value',
            'coupon_code',
            'linked_phone_number',
            'is_active',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
