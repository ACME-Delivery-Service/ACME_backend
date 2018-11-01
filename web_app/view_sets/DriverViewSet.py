from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class DriverViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def current(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='co-contact', permission_classes=[IsAuthenticated])
    def co_contact(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['POST', 'GET'], permission_classes=[IsAuthenticated])
    def location(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request):
        return Response(status=HTTP_200_OK)
