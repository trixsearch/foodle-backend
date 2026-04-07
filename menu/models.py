from django.db import models

from foodle_core.timebase import TimeStampedModel


class MenuCategory(TimeStampedModel):
    class FoodType(models.TextChoices):
        VEG = 'veg', 'Veg'
        NON_VEG = 'non_veg', 'Non-veg'
        VEGAN = 'vegan', 'Vegan'

    name = models.CharField(max_length=128)
    food_type = models.CharField(max_length=16, choices=FoodType.choices)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Menu categories'

    def __str__(self):
        return self.name


class MenuItem(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        MenuCategory,
        on_delete=models.PROTECT,
        related_name='items',
    )
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_slab = models.ForeignKey(
        'finance.TaxSlab',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='menu_items',
    )
    short_code = models.CharField(max_length=32, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('category', 'name')

    def __str__(self):
        return self.name


class MenuVariation(TimeStampedModel):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='variations',
    )
    name = models.CharField(max_length=128)
    price_adjustment = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ('menu_item', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=('menu_item', 'name'),
                name='menu_menuvariation_item_name_uniq',
            ),
        ]

    def __str__(self):
        return f'{self.menu_item.name} — {self.name}'


class AddOn(TimeStampedModel):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Add-on'
        verbose_name_plural = 'Add-ons'

    def __str__(self):
        return self.name
