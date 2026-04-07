from django.db import models

from foodle_core.timebase import TimeStampedModel


class TaxSlab(TimeStampedModel):
    name = models.CharField(max_length=128)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class DiscountConfig(TimeStampedModel):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        FLAT_AMOUNT = 'flat_amount', 'Flat amount'

    name = models.CharField(max_length=128)
    discount_type = models.CharField(max_length=32, choices=DiscountType.choices)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    coupon_code = models.CharField(max_length=64, blank=True)
    linked_phone_number = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
