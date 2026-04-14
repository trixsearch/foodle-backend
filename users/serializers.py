import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from customers.models import Client

from .utils import subdomain_to_schema_name

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'role',
        )
        read_only_fields = fields

    def get_full_name(self, obj):
        parts = [obj.first_name or '', obj.last_name or '']
        return ' '.join(p for p in parts if p).strip() or obj.username


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=['CASHIER', 'CHEF', 'MANAGER'])

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'role',
        )

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Email already in use.')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already in use.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        validated_data['username'] = email
        validated_data['email'] = email
        return User.objects.create_user(password=password, **validated_data)


class TenantProvisionSerializer(serializers.Serializer):
    restaurant_name = serializers.CharField(max_length=255)
    subdomain = serializers.CharField(max_length=63)
    plan_type = serializers.ChoiceField(choices=['basic', 'premium'])
    owner_first_name = serializers.CharField(max_length=150)
    owner_last_name = serializers.CharField(max_length=150)
    owner_email = serializers.EmailField()
    owner_password = serializers.CharField(min_length=8, write_only=True)

    def validate_subdomain(self, value):
        value = value.strip().lower()
        if not re.match(r'^[a-z][a-z0-9-]{1,62}$', value):
            raise serializers.ValidationError(
                'Subdomain must start with a letter and use lowercase letters, digits, or hyphens.',
            )
        schema_name = subdomain_to_schema_name(value)
        if Client.objects.filter(schema_name=schema_name).exists():
            raise serializers.ValidationError('This subdomain is already taken.')
        return value


class SaasTenantOutSerializer(serializers.ModelSerializer):
    subdomain = serializers.SerializerMethodField()
    schema_name_display = serializers.CharField(source='schema_name', read_only=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'subdomain',
            'schema_name_display',
            'plan_type',
            'subscription_end_date',
            'is_active',
        )

    def get_subdomain(self, obj):
        dom = obj.domains.filter(is_primary=True).first() or obj.domains.first()
        if not dom:
            return ''
        return dom.domain.split('.')[0]
