from datetime import timedelta

from django.db import connection
from django.http import JsonResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name


class SubscriptionCheckMiddleware(MiddlewareMixin):
    """
    Blocks tenant-schema HTTP requests when the tenant is past
    subscription_end_date + 15 days grace.
    """

    def process_request(self, request):
        tenant = getattr(request, 'tenant', None)
        if tenant is None:
            return None
        if connection.schema_name == get_public_schema_name():
            return None

        grace_end = tenant.subscription_end_date + timedelta(days=15)
        if timezone.now().date() > grace_end:
            return JsonResponse(
                {
                    'detail': (
                        'Your Foodle subscription has expired. '
                        'Please renew your plan to continue.'
                    )
                },
                status=403,
            )
        return None
