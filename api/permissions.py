from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff
            or request.user.role in ("admin", "django_admin")
        )


class CustomerAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class MethodAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "POST":
            return request.user.is_authenticated
        else:
            return request.user.is_staff or request.user.role in ("admin", "django_admin")

