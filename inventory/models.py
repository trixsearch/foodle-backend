from django.db import models

from foodle_core.timebase import TimeStampedModel


class RawMaterial(TimeStampedModel):
    class Unit(models.TextChoices):
        KG = 'kg', 'KG'
        LTR = 'ltr', 'LTR'
        GRAM = 'gram', 'Gram'
        PIECE = 'piece', 'Piece'

    name = models.CharField(max_length=255)
    unit_of_measurement = models.CharField(max_length=16, choices=Unit.choices)
    current_stock = models.DecimalField(max_digits=14, decimal_places=4)
    minimum_stock_alert = models.DecimalField(max_digits=14, decimal_places=4)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(TimeStampedModel):
    menu_item = models.OneToOneField(
        'menu.MenuItem',
        on_delete=models.CASCADE,
        related_name='recipe',
    )

    class Meta:
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'Recipe for {self.menu_item.name}'


class RecipeIngredient(TimeStampedModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.PROTECT,
        related_name='recipe_usages',
    )
    quantity_required = models.DecimalField(max_digits=14, decimal_places=4)

    class Meta:
        ordering = ('recipe', 'raw_material')
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'raw_material'),
                name='inventory_recipeingredient_recipe_material_uniq',
            ),
        ]

    def __str__(self):
        return f'{self.recipe.menu_item.name}: {self.raw_material.name} ({self.quantity_required})'
