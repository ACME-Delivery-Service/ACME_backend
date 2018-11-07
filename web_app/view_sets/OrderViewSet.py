from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from web_app.serializers import *


class OrderViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def status(self, request):
        status = AcmeOrderStatus.status

        if request.method == 'GET':
            return Response(status, status=HTTP_200_OK)

        elif request.method == 'POST':
            serializer = AcmeOrderStatus(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        if not pk:
            return Response({'msg': 'No ID provided'}, HTTP_400_BAD_REQUEST)

        return Response({
            'id': pk,
            'delivery_period': {
                'start': '2018-12-25 12:20:00',
                'end': '2018-01-25 10:10:00'
            },
            'priority': 242,
            'address_from': {
                'address': 'Infinite loop, 1, Cupertino, CA, USA',
                'location': {
                    'latitude': 12343526.31,
                    'longitude': 42445698.7
                }
            },
            'address_to': {
                'address': 'Infinite loop, 1, Cupertino, CA, USA',
                'location': {
                    'latitude': 35664564.31,
                    'longitude': 67367546.3
                }
            },
            'description': 'The client asked not to knock on the door, just leave it.',
            'parcels_info': [
                {
                    'id': 123312,
                    'weight': 1.38,
                    'dimensions': {
                        'x': 123.0,
                        'y': 123.0,
                        'z': 123.0
                    },
                    'shape': 'Unsupported yet',
                    'description': 'Please be cautious while moving this one.'
                }
            ],
            'customer_info': {
                'id': 1243,
                'contacts': {
                    'first_name': 'Johnathan',
                    'last_name': 'Morrison',
                    'phone_number': '+1123412341234'
                },
            },
            'status': 'pending'
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def location(self, request):
        return Response({
            'id': 1,
            'location': {
                'latitude': 35664564.31,
                'longitude': 67367546.3
            }
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def assign(self, request):
        if request.method == 'GET':
            return Response({
                'id': 1,
                'location': {
                    'latitude': 35664564.31,
                    'longitude': 67367546.3
                }
            }, status=HTTP_200_OK)

        elif request.method == 'POST':
            order_id = request.data.get("order_id")
            deriver_id = request.data.get("deriver_id")

            return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request):
        queryset = AcmeOrder.objects.all()
        serializer = AcmeOrder(queryset, many=True)
        return Response(serializer.data)
