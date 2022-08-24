from rest_framework.permissions import BasePermission

class IsProfileOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "GET" or request.user.is_staff or request.user and request.user.id == obj.id 