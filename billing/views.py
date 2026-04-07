from rest_framework import viewsets

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
from .serializers import (
    DiningAreaSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    KOTSerializer,
    PaymentSerializer,
    PettyCashSerializer,
    TableSerializer,
    VoidLogSerializer,
)


class DiningAreaViewSet(viewsets.ModelViewSet):
    queryset = DiningArea.objects.all()
    serializer_class = DiningAreaSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.select_related('area').all()
    serializer_class = TableSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = (
        Invoice.objects.select_related(
            'table',
            'table__area',
            'waiter',
            'cashier',
            'discount_applied',
        )
        .prefetch_related(
            'items__menu_item__category',
            'items__menu_item__tax_slab',
            'kots',
        )
        .all()
    )
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.select_related(
        'invoice',
        'menu_item',
        'menu_item__category',
        'menu_item__tax_slab',
    ).all()
    serializer_class = InvoiceItemSerializer


class KOTViewSet(viewsets.ModelViewSet):
    queryset = KOT.objects.select_related('invoice').all()
    serializer_class = KOTSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice').all()
    serializer_class = PaymentSerializer


class VoidLogViewSet(viewsets.ModelViewSet):
    queryset = VoidLog.objects.select_related('invoice', 'voided_by').all()
    serializer_class = VoidLogSerializer


class PettyCashViewSet(viewsets.ModelViewSet):
    queryset = PettyCash.objects.select_related('user').all()
    serializer_class = PettyCashSerializer
