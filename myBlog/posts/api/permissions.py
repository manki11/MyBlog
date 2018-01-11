from rest_framework.permissions import BasePermission, SAFE_METHODS


class isOwnerorReadOnly(BasePermission):
    message = "You must be the owner of this object"
    my_safe_method = ['GET', 'PUT', 'POST']

    def has_object_permission(self, request, view, obj):
        if not request.method in SAFE_METHODS:
            return False
        return obj.user == request.user
