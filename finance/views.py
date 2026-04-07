from rest_framework import viewsets

from .models import DiscountConfig, TaxSlab
from .serializers import DiscountConfigSerializer, TaxSlabSerializer


class TaxSlabViewSet(viewsets.ModelViewSet):
    queryset = TaxSlab.objects.all()
    serializer_class = TaxSlabSerializer


class DiscountConfigViewSet(viewsets.ModelViewSet):
    queryset = DiscountConfig.objects.all()
    serializer_class = DiscountConfigSerializer
