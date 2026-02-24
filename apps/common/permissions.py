from rest_framework.permissions import BasePermission, IsAuthenticated

class IsSupplier(BasePermission):
    """
    Разрешение только для поставщиков
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 'supplier')

class IsBuyer(BasePermission):
    """
    Разрешение только для покупателей
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 'buyer')

class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение на редактирование только владельцу
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user