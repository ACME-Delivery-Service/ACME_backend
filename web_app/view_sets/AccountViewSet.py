from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from web_app.exceptions import AcmeAPIException
from web_app.permissions import IsAuthenticatedOrMeta


class AccountViewSet(viewsets.ViewSet):

    # @csrf_exempt
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise AcmeAPIException('Please provide both email and password')
        if email != 'j.doe@innopolis.ru' or password != '12345678':
            raise AcmeAPIException('Invalid login credentials')

        token, _ = Token.objects.get_or_create()
        return Response({'token': token.key}, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticatedOrMeta])
    def logout(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticatedOrMeta])
    def info(self, request):
        return Response({
            'id': 1,
            'email': 'j.doe@innopolis.ru',
            'location': 'RU',
            'avatar_url': 'http://fanaru.com/avatar/image/240677-avatar-http-www-hdwallpapers-in-walls-jake_sully_avatar_disguise-wide-jpg.jpg',
            'contacts': {
                'address': 'Unsupported yet',
                'phone_number': '8(800)555-35-35',
                'additional_info': 'Unsupported yet',
                'first_name': 'Evgeny',
                'last_name': 'Baticov',
                'position': 'Driver helper',
                'company': 'Unsupported yet',
            }
        }, status=HTTP_200_OK)
