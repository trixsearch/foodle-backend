from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DiningAreaViewSet,
    InvoiceItemViewSet,
    InvoiceViewSet,
    KOTViewSet,
    PaymentViewSet,
    PettyCashViewSet,
    TableViewSet,
    VoidLogViewSet,
)

router = DefaultRouter()
router.register(r'dining-areas', DiningAreaViewSet, basename='diningarea')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoiceitem')
router.register(r'kots', KOTViewSet, basename='kot')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'void-logs', VoidLogViewSet, basename='voidlog')
router.register(r'petty-cash', PettyCashViewSet, basename='pettycash')

urlpatterns = [
    path('', include(router.urls)),
]
