from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 로그인 안해도 읽기 가능
        if request.method in permissions.SAFE_METHODS:
            return True
        # 로그인해야 읽기 가능

        return obj.user_id == request.user