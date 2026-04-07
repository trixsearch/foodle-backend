from django.conf import settings
from django.db import models

from foodle_core.timebase import TimeStampedModel


class DiningArea(TimeStampedModel):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Table(TimeStampedModel):
    area = models.ForeignKey(
        DiningArea,
        on_delete=models.PROTECT,
        related_name='tables',
    )
    table_number = models.CharField(max_length=32)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    class Meta:
        ordering = ('area', 'table_number')
        constraints = [
            models.UniqueConstraint(
                fields=('area', 'table_number'),
                name='billing_table_area_number_uniq',
            ),
        ]

    def __str__(self):
        return f'{self.area.name} — Table {self.table_number}'


class Invoice(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PAID = 'paid', 'Paid'
        VOIDED = 'voided', 'Voided'

    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices',
    )
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=32, null=True, blank=True)
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='waiter_invoices',
    )
    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cashier_invoices',
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    discount_applied = models.ForeignKey(
        'finance.DiscountConfig',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices',
    )
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax_total = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    is_synced = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        label = self.pk if self.pk is not None else 'new'
        return f'Invoice #{label} ({self.get_status_display()})'


class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
    )
    menu_item = models.ForeignKey(
        'menu.MenuItem',
        on_delete=models.PROTECT,
        related_name='invoice_items',
    )
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.menu_item.name} × {self.quantity} on invoice #{self.invoice_id}'


class KOT(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PREPARING = 'preparing', 'Preparing'
        READY = 'ready', 'Ready'
        DELIVERED = 'delivered', 'Delivered'

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='kots',
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ('invoice', 'id')
        verbose_name = 'KOT'
        verbose_name_plural = 'KOTs'

    def __str__(self):
        return f'KOT #{self.pk} ({self.get_status_display()}) — Invoice #{self.invoice_id}'


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'
        UPI = 'upi', 'UPI'

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    payment_method = models.CharField(max_length=16, choices=Method.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        ordering = ('invoice', 'id')

    def __str__(self):
        return f'{self.get_payment_method_display()} {self.amount} — Invoice #{self.invoice_id}'


class VoidLog(TimeStampedModel):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='void_logs',
    )
    voided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='void_logs',
    )
    reason = models.CharField(max_length=255)
    voided_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-voided_at',)

    def __str__(self):
        return f'Void invoice #{self.invoice_id} at {self.voided_at}'


class PettyCash(TimeStampedModel):
    class TransactionType(models.TextChoices):
        IN = 'in', 'In'
        OUT = 'out', 'Out'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='petty_cash_entries',
    )
    transaction_type = models.CharField(max_length=8, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=255)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Petty cash entry'
        verbose_name_plural = 'Petty cash entries'

    def __str__(self):
        return f'{self.get_transaction_type_display()} {self.amount} — {self.reason[:40]}'
