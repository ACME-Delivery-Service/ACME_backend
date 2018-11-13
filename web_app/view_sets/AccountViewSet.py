from django.conf import settings
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from web_app.exceptions import AcmeAPIException
from web_app.models import AcmeUser
from web_app.permissions import IsAuthenticatedOrMeta
from web_app.serializers_default import ContactSerializer


class AccountViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        app_key = request.data.get("app_key")

        if not email or not password:
            raise AcmeAPIException('Please provide both email and password')
        if settings.REQUIRE_APP_KEY and not app_key:
            raise AcmeAPIException('Please provide app key')

        user = authenticate(request, email=email, password=password, app_key=app_key)
        if not user:
            raise AcmeAPIException('Invalid login credentials')

        token, _ = Token.objects.get_or_create(user_id=user.id)
        return Response({'token': token.key}, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticatedOrMeta])
    def logout(self, request):
        token = Token.objects.get(user_id=request.user.id)
        token.delete(None, True)

        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticatedOrMeta])
    def info(self, request):
        user = request.user  # type: AcmeUser
        contacts = ContactSerializer(user.contacts)

        return Response({
            'id': user.id,
            'email': user.email,
            'location': user.region,
            'avatar_url': user.get_avatar(),
            'contacts': contacts.data
        }, status=HTTP_200_OK)
