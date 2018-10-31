from enum import Enum
from rest_framework.compat import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


class OrderViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def status(self, request):
        status = request.data.get("status")
        delivery_order_id = request.data.get("delivery_order_id")
        user_token = request.data.get("token")

        if request.method == 'GET':
            return Response(status=HTTP_200_OK)

        elif request.method == 'POST':
            if status == 'finished':
                return Response(status=HTTP_200_OK)
            elif status == 'in_process':
                return Response(status=HTTP_200_OK)
            else:
                return Response({'msg': 'pending'}, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request):
        return Response({
            'id': 1,
            'delivery_period': {'start': '28.09.2018', 'end': '15.10.2018'},
            'priority': '123',
            'address_from': {
                'address': 'Infinite loop, 1, Cupertino, CA, USA',
                'location': {
                    'latitude': 12343526.31,
                    'longitude': 42445698.7
                }},
            'address_to': {
                'address': 'Infinite loop, 1, Cupertino, CA, USA',
                'location': {
                    'latitude': 35664564.31,
                    'longitude': 67367546.3
                }
            },
            'description': 'The client asked not to knock on the door, just leave it.',
            'parcel_info': {
                'id': '#12345125BAC',
                'weight': '1 kg',
                'dimensions': {
                    'x': '123.0',
                    'y': '123.0',
                    'z': '123.0'
                },
                'shape': 'Unsupported yet',
                'description': 'Please be cautious while moving this one.'
            },
            'customer_info': {
                'first_name': 'Johnathan',
                'last_name': 'Morrison',
                'phone_number': '+1123412341234'
            },
            'status': 'Unsupported yet'
        }
            , status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def location(self, request):
        return Response({
            'id': 1,
            'location': {
                'latitude': 35664564.31,
                'longitude': 67367546.3
            }
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def assign(self, request):
        return Response({
            'id': 1,
            'driver_id': 123
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request):
        return Response({
            'total_count': 123,
            'results': [{
                'id': 1,
                'delivery_period': {
                    'start': '23.04.2018',
                    'end': '20.07.2018'
                },
                'priority': 123,
                'address_to': {
                    'address': 'Infinite loop, 1, Cupertino, CA, USA',
                    'location': {
                        'latitude': 35664564.31,
                        'longitude': 67367546.3
                    }
                },
                'address_from': {
                    'address': 'Infinite loop, 1, Cupertino, CA, USA',
                    'location': {
                        'latitude': 12343526.31,
                        'longitude': 42445698.3
                    }
                }
            }]
        }, status=HTTP_200_OK)
