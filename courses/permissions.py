from rest_framework import permissions

class IsAdminOrAuthenticated(permissions.BasePermission):
    """
    Разрешение для редактирования курсов только администраторам,
    а доступ к курсам - только авторизованным пользователям.
    """

    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS запросы для всех пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить доступ только администраторам для других методов
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Разрешить доступ к курсам только авторизованным пользователям
        # после оплаты
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверка оплаты для просмотра объектов
        if request.user.is_authenticated and obj.is_paid:
            return True

        # Разрешить доступ только администраторам для других действий
        return request.user and request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение для администраторов на редактирование и удаление,
    но только для чтения для всех остальных пользователей.
    """

    def has_permission(self, request, view):
        # Разрешить GET, HEAD, OPTIONS запросы для всех пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить доступ только администраторам для других методов
        return request.user and request.user.is_staff