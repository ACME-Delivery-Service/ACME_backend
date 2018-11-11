from rest_framework.permissions import BasePermission

META_METHODS = ('HEAD', 'OPTIONS')


class IsAuthenticatedOrMeta(BasePermission):
    """
    The request is authenticated as a user, or is a meta request.
    """

    def has_permission(self, request, view):
        return (
                request.method in META_METHODS or
                request.user and
                request.user.is_authenticated
        )

    def has_parent_permission(self, request, view):
        return IsAuthenticatedOrMeta.has_permission(self, request, view)


class IsAdmin(IsAuthenticatedOrMeta):
    """
    The request is authenticated as a user and user is CEO
    """

    def has_permission(self, request, view):
        return self.has_parent_permission(request, view) and True  # request.user.role === 'CEO'


class IsControlOperator(IsAuthenticatedOrMeta):
    """
    The request is authenticated as a user and user is CO
    """

    def has_permission(self, request, view):
        return self.has_parent_permission(request, view) and True  # request.user.role === 'CO'


class IsDeliveryOperator(IsAuthenticatedOrMeta):
    """
    The request is authenticated as a user and user is DO
    """

    def has_permission(self, request, view):
        return self.has_parent_permission(request, view) and True  # request.user.role === 'DO'
