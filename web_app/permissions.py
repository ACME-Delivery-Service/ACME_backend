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
