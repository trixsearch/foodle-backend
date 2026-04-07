from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


def default_feature_flags():
    return {'zomato_sync': False, 'loyalty': True}


class Client(TenantMixin):
    class PlanType(models.TextChoices):
        BASIC = 'basic', 'Basic'
        PREMIUM = 'premium', 'Premium'
        ENTERPRISE = 'enterprise', 'Enterprise'

    name = models.CharField(max_length=255)
    plan_type = models.CharField(
        max_length=32,
        choices=PlanType.choices,
    )
    subscription_end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    feature_flags = models.JSONField(default=default_feature_flags)
    created_on = models.DateTimeField(auto_now_add=True)

    auto_create_schema = True
    auto_drop_schema = False

    class Meta:
        verbose_name = 'Client (tenant)'
        verbose_name_plural = 'Clients (tenants)'

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'
