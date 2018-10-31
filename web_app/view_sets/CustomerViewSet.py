from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CustomerViewSet(viewsets.ViewSet):

    def info(self, request):
        return Response({'name': 'John Vorbob',
                         'photo': '',
                         'phone_number': '+79991764478'},
                        status=HTTP_200_OK)
