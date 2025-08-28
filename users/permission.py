from rest_framework.permissions import BasePermission

class IsModer(BasePermission):
    """
    Разрешение для модераторов: могут просматривать и редактировать любые объекты,
    но не могут создавать и удалять.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()

class IsOwner(BasePermission):
    """
    Доступ только владельцу объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
