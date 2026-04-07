from django.contrib.auth import get_user_model
from rest_framework import serializers

from finance.models import DiscountConfig
from finance.serializers import DiscountConfigSerializer
from menu.serializers import MenuItemSerializer

from .models import (
    DiningArea,
    Invoice,
    InvoiceItem,
    KOT,
    Payment,
    PettyCash,
    Table,
    VoidLog,
)

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role')
        read_only_fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role')


class DiningAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiningArea
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class TableSerializer(serializers.ModelSerializer):
    area_detail = DiningAreaSerializer(source='area', read_only=True)
    area = serializers.PrimaryKeyRelatedField(
        queryset=DiningArea.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Table
        fields = (
            'id',
            'area',
            'area_detail',
            'table_number',
            'capacity',
            'is_occupied',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'area_detail', 'created_at', 'updated_at')


class InvoiceItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = InvoiceItem
        fields = (
            'id',
            'menu_item',
            'menu_item_detail',
            'quantity',
            'price_per_unit',
            'tax_amount',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'menu_item_detail', 'created_at', 'updated_at')


class KOTNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = KOT
        fields = ('id', 'status', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'status', 'notes', 'created_at', 'updated_at')


class KOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = KOT
        fields = (
            'id',
            'invoice',
            'status',
            'notes',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)
    kots = KOTNestedSerializer(many=True, read_only=True)

    discount_applied_detail = DiscountConfigSerializer(
        source='discount_applied',
        read_only=True,
    )
    discount_applied = serializers.PrimaryKeyRelatedField(
        queryset=DiscountConfig.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )

    table_detail = TableSerializer(source='table', read_only=True)
    table = serializers.PrimaryKeyRelatedField(
        queryset=Table.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )

    waiter_detail = UserBriefSerializer(source='waiter', read_only=True)
    waiter = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
        write_only=True,
    )

    cashier_detail = UserBriefSerializer(source='cashier', read_only=True)
    cashier = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Invoice
        fields = (
            'id',
            'table',
            'table_detail',
            'customer_name',
            'customer_phone',
            'waiter',
            'waiter_detail',
            'cashier',
            'cashier_detail',
            'status',
            'discount_applied',
            'discount_applied_detail',
            'subtotal',
            'tax_total',
            'discount_amount',
            'grand_total',
            'is_synced',
            'items',
            'kots',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'table_detail',
            'waiter_detail',
            'cashier_detail',
            'discount_applied_detail',
            'kots',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        invoice = super().update(instance, validated_data)
        if items_data is not None:
            invoice.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'invoice',
            'payment_method',
            'amount',
            'transaction_id',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class VoidLogSerializer(serializers.ModelSerializer):
    voided_by_detail = UserBriefSerializer(source='voided_by', read_only=True)
    voided_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = VoidLog
        fields = (
            'id',
            'invoice',
            'voided_by',
            'voided_by_detail',
            'reason',
            'voided_at',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'voided_by_detail',
            'voided_at',
            'created_at',
            'updated_at',
        )


class PettyCashSerializer(serializers.ModelSerializer):
    user_detail = UserBriefSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = PettyCash
        fields = (
            'id',
            'user',
            'user_detail',
            'transaction_type',
            'amount',
            'reason',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user_detail', 'created_at', 'updated_at')
