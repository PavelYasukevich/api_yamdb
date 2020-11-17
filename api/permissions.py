from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            (request.user.is_staff or request.user.role in ("admin", "django_admin"))
        )
