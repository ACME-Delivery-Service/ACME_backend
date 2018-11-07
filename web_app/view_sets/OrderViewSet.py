from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class OrderViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def status(self, request):
        status = request.data.get("status")
        delivery_order_id = request.data.get("delivery_order_id")

        if request.method == 'GET':
            return Response(status=HTTP_200_OK)

        elif request.method == 'POST':
            if status == 'finished':
                return Response(status=HTTP_200_OK)
            elif status == 'in_process':
                return Response(status=HTTP_200_OK)
            else:
                return Response({'msg': 'pending'}, status=HTTP_200_OK)

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
            'created_at': '1970-01-01 00:00:00',
            'updated_at': '1980-01-01 00:00:00',
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
            'driver_info': {
                'id': 1234,
                'avatar': 'http',
                'contacts': {
                    'first_name': 'Johnathan',
                    'last_name': 'Morrison',
                    'phone_number': '+1123412341234'
                },
            },
            'location': {
                'latitude': 35664564.31,
                'longitude': 67367546.3
            },
            'status': 'en_route',
            'delivery_status': 'pending'
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
        return Response({
            'total_count': 123,
            'results': [{
                'id': 1,
                'delivery_period': {
                    'start': '2018-12-25 12:20:00',
                    'end': '2018-01-25 10:10:00'
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
                },
                'status': 'en_route',
                'is_assigned': True,
                'delivery_operator': {
                    'id': 123,
                    'avatar': 'http',
                    'contacts': {
                        'phone_number': '+757488',
                    }
                },
            }]
        }, status=HTTP_200_OK)
