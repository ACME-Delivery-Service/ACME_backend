from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import (
    check_password, make_password,
)
from django.conf import settings

from web_app.exceptions import AcmeAPIException
from web_app.models import AcmeUser, UserRole, AcmeRoles

APP_KEYS = settings.APP_KEYS

ROLE_APP = {
    AcmeRoles.CEO.value: 'web',
    AcmeRoles.CO.value: 'web',
    AcmeRoles.DO.value: 'mobile',
}


class UserHelper:
    _user = None  # type: AcmeUser

    def __init__(self, user):
        self._user = user

    def check_password(self, password):
        return check_password(password, self._user.password)

    @staticmethod
    def get_password_hash(password):
        return make_password(password)

    def get_role(self):
        return self._user.get_role()


class AuthBackend(ModelBackend):
    """
    Authenticates user
    """

    def get_user(self, user_id):
        return AcmeUser.objects.get(pk=user_id)

    def authenticate(self, request, email=None, username=None, password=None, app_key=None, **kwargs):
        if email is None:
            email = username

        try:
            user = AcmeUser.objects.get(email=email)
            helper = UserHelper(user)
        except AcmeUser.DoesNotExist:
            pass
        else:
            if helper.check_password(password):
                if not self.check_app_key(helper, app_key):
                    raise AcmeAPIException('Invalid app key supplied')
                return user

    @staticmethod
    def check_app_key(helper, app_key):
        if not settings.REQUIRE_APP_KEY:
            return True

        role = helper.get_role()
        print('WARNING: No user role found')
        if not role:
            return False

        key_type = ROLE_APP[role]
        true_key = APP_KEYS[key_type]

        return true_key == app_key

    def _get_user_permissions(self, user_obj):
        return set()

    def _get_group_permissions(self, user_obj):
        return set()
