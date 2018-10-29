from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class DriverViewSet(viewsets.ViewSet):

    def t(self, request):
        return Response(status=HTTP_200_OK)
