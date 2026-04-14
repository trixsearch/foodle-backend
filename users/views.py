import logging
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import connection
from django_tenants.utils import get_public_schema_name, schema_context
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import Client, Domain
from customers.serializers import TenantBriefSerializer

from .permissions import IsCafeOwnerOrSuperAdmin, IsSuperAdmin
from .serializers import (
    SaasTenantOutSerializer,
    TenantProvisionSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from .utils import subdomain_to_schema_name

logger = logging.getLogger(__name__)

User = get_user_model()


class LoginAPIView(APIView):
    """
    POST username + password.
    Resolves the correct schema via django-tenants from the Host header
    (public schema for SaaS host, tenant schema for restaurant subdomain).
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)


class CurrentTenantAPIView(APIView):
    """
    Returns the restaurant (Client) for the current hostname when not on the public SaaS host.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        tenant = getattr(request, 'tenant', None)
        if tenant is None or getattr(tenant, 'schema_name', None) == get_public_schema_name():
            return Response(
                {'detail': 'No tenant context for this host.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(TenantBriefSerializer(tenant).data)


class SaasTenantListCreateView(APIView):
    """List or create tenants (SuperAdmin, public schema only)."""

    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request, *args, **kwargs):
        if connection.schema_name != get_public_schema_name():
            return Response(
                {'detail': 'List tenants only from the platform host.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        tenants = Client.objects.all().order_by('name')
        return Response(SaasTenantOutSerializer(tenants, many=True).data)

    def post(self, request, *args, **kwargs):
        if connection.schema_name != get_public_schema_name():
            return Response(
                {'detail': 'Provision tenants only from the platform host.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        ser = TenantProvisionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        subdomain = d['subdomain']
        schema_name = subdomain_to_schema_name(subdomain)

        tenant = None
        try:
            tenant = Client(
                schema_name=schema_name,
                name=d['restaurant_name'].strip(),
                plan_type=d['plan_type'],
                subscription_end_date=date.today() + timedelta(days=365),
            )
            tenant.save()
            domain_host = f'{subdomain}.localhost'
            Domain.objects.create(domain=domain_host, tenant=tenant, is_primary=True)
            email = d['owner_email'].strip().lower()
            with schema_context(tenant.schema_name):
                User.objects.create_user(
                    username=email,
                    email=email,
                    password=d['owner_password'],
                    first_name=d['owner_first_name'].strip(),
                    last_name=d['owner_last_name'].strip(),
                    role=User.Role.CAFE_OWNER,
                )
        except Exception:
            logger.exception('Tenant provisioning failed')
            try:
                if tenant is not None and getattr(tenant, 'pk', None):
                    tenant.delete(force_drop=True)
            except Exception:
                logger.exception('Could not roll back tenant')
            return Response(
                {'detail': 'Provisioning failed. Please try again or contact support.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            SaasTenantOutSerializer(tenant).data,
            status=status.HTTP_201_CREATED,
        )


class StaffUserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Tenant-schema staff listing and creation (cafe owner / superadmin).
    """

    permission_classes = [IsAuthenticated, IsCafeOwnerOrSuperAdmin]

    def get_queryset(self):
        if connection.schema_name == get_public_schema_name():
            return User.objects.none()
        return User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        if connection.schema_name == get_public_schema_name():
            return Response(
                {'detail': 'Staff API is only available on a restaurant subdomain.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if connection.schema_name == get_public_schema_name():
            return Response(
                {'detail': 'Staff API is only available on a restaurant subdomain.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)
