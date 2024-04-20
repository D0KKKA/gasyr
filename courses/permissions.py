from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Пользователи, имеющие административные права, могут выполнять любые действия,
    в то время как обычные пользователи могут выполнять только чтение.
    """
    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS запросы для всех пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверить, является ли пользователь администратором
        return request.user and request.user.is_staff


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее чтение для неаутентифицированных пользователей,
    но требующее аутентификацию для любых других операций.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )