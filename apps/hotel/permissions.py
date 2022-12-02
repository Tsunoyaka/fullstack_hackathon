from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user


class IsManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin and request.user == obj.user