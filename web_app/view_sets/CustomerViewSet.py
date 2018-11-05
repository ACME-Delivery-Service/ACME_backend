from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CustomerViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request):
        return Response({
            'id': 1243,
            'contacts': {
                'first_name': 'Johnathan',
                'last_name': 'Morrison',
                'phone_number': '+1123412341234'
            },
        }, status=HTTP_200_OK)
