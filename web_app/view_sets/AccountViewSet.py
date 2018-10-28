from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from web_app.models import DeliveryOperator


class AccountViewSet(viewsets.ViewSet):

    # @csrf_exempt
    # @api_view(["POST"])
    # @permission_classes((AllowAny,))
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'msg': 'Please provide both email and password'}, status=HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create()
        return Response({'token': token.key}, status=HTTP_200_OK)
