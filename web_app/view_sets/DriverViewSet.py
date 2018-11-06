from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class DriverViewSet(viewsets.ViewSet):

    def extract_orders_list(self, driver_id, status, pagination):
        pending_orders = [
            {
                'id': 1,
                'delivery_period': {
                    'start': '2018-10-25 22:20:00',
                    'end': '2018-11-25 20:10:00'
                },
                'priority': 2,
                'address_from': {
                    'address': 'Infinite, 100, Cup, CA, USA',
                    'location': {
                        'latitude': 12343526.31,
                        'longitude': 42445698.7
                    }
                },
                'address_to': {
                    'address': 'Inf loop, 1, Cuper, CA, USA',
                    'location': {
                        'latitude': 35664564.31,
                        'longitude': 67367546.3
                    }
                }
            },
            {
                'id': 2,
                'delivery_period': {
                    'start': '2018-10-25 22:20:00',
                    'end': '2018-11-25 20:10:00'
                },
                'priority': 2,
                'address_from': {
                    'address': 'Infinite, 100, Cup, CA, USA',
                    'location': {
                        'latitude': 12343526.31,
                        'longitude': 42445698.7
                    }
                },
                'address_to': {
                    'address': 'Inf loop, 1, Cuper, CA, USA',
                    'location': {
                        'latitude': 35664564.31,
                        'longitude': 67367546.3
                    }
                }
            }
        ]

        current_orders = [
            {
                'id': 3,
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
                    }},
                'address_to': {
                    'address': 'Infinite loop, 1, Cupertino, CA, USA',
                    'location': {
                        'latitude': 35664564.31,
                        'longitude': 67367546.3
                    }
                }
            },
            {
                'id': 4,
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
                }
            }
        ]

        corders = pending_orders if status == 'pending' else current_orders

        return {
            'total_count': len(corders),
            'results': corders
        }

    def format_pagination(self, request):
        limit = request.get('limit')
        offset = request.get('offset')

        if not limit:
            limit = None
        if not offset:
            offset = 0

        return limit, offset

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        return Response(self.extract_orders_list(1, 'pending', self.format_pagination(request)), status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def current(self, request):
        return Response(self.extract_orders_list(1, 'in_progress', self.format_pagination(request)), status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='co-contact', permission_classes=[IsAuthenticated])
    def co_contact(self, request):
        return Response({
            'id': 1243,
            'contacts': {
                'first_name': 'Johnathan',
                'last_name': 'Morrison',
                'phone_number': '+1123412341234'
            }
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['POST', 'GET'], permission_classes=[IsAuthenticated])
    def location(self, request):
        # todo
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request):
        # todo
        return Response(status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request):
        # todo
        return Response(status=HTTP_200_OK)
