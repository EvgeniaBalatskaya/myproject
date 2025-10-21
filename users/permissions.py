from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """
    Модератор может просматривать и редактировать объекты,
    но не может создавать и удалять.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name="Moderators").exists():
            if getattr(view, "action", None) in ["create", "destroy"]:
                return False
            return True
        return False


class IsOwner(BasePermission):
    """Разрешение владельцу объекта."""
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner", None) == request.user


class IsOwnerOrModer(BasePermission):
    """Разрешение для объекта: владелец или модератор."""
    def has_object_permission(self, request, view, obj):
        is_owner = getattr(obj, 'owner', None) == request.user
        is_moder = request.user.groups.filter(name="Moderators").exists()
        return is_owner or is_moder


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешение для объекта: владелец или админ.
    Модератор **не может** удалять.
    """
    def has_object_permission(self, request, view, obj):
        is_owner = getattr(obj, 'owner', None) == request.user
        is_admin = request.user.is_staff or request.user.is_superuser
        return is_owner or is_admin
