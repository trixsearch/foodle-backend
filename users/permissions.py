from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'role', None) == 'SUPERADMIN',
        )


class IsCafeOwnerOrSuperAdmin(BasePermission):
    """Tenant staff management: cafe owner or superadmin (if present in tenant schema)."""

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        role = getattr(user, 'role', None)
        return role in ('CAFE_OWNER', 'SUPERADMIN')
