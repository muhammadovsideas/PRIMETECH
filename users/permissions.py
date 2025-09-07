from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role == "ADMIN":
            return True
        return False

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and  request.user.is_authenticated and request.user.role == "USER":
            return True
        return False