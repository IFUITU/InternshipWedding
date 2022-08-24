from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method == "GET" or request.user and request.user.is_staff)

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or request.user ==  obj.author # or request.user.is_staff