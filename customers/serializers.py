from rest_framework import serializers

from .models import Client


class TenantBriefSerializer(serializers.ModelSerializer):
    """Public tenant metadata for the current hostname (django-tenants context)."""

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'plan_type',
            'subscription_end_date',
            'is_active',
            'feature_flags',
        )
        read_only_fields = fields
