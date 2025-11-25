from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, "user") and obj.user == request.user
    
