from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from web_app.serializers_default import *
import json
import random
from django.http import HttpResponse, JsonResponse


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
                    'address': 'Спортивная ул., 134-136, Иннополис, Респ. Татарстан, 422594',
                    'location': {
                        'latitude': 55.750194,
                        'longitude': 48.742944
                    }
                },
                'address_to': {
                    'address': 'Unnamed Road, Иннополис, Респ. Татарстан, 422591',
                    'location': {
                        'latitude': 55.748224,
                        'longitude': 48.741482
                    }
                },
                'delivery_status': 'pending',
            },
            {
                'id': 2,
                'delivery_period': {
                    'start': '2018-10-25 22:20:00',
                    'end': '2018-11-25 20:10:00'
                },
                'priority': 2,
                'address_from': {
                    'address': 'Университетская ул., Иннополис, Респ. Татарстан, 422594',
                    'location': {
                        'latitude': 55.750138,
                        'longitude': 48.753595
                    }
                },
                'address_to': {
                    'address': 'Inf loop, 1, Cuper, CA, USA',
                    'location': {
                        'latitude': 35664564.31,
                        'longitude': 67367546.3
                    }
                },
                'delivery_status': 'pending',
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
                    'address': 'Центральная ул., Казань, Респ. Татарстан, 420049',
                    'location': {
                        'latitude': 55.776223,
                        'longitude': 49.148516
                    }},
                'address_to': {
                    'address': 'Вахитовский р-н, Казань, Респ. Татарстан, 420021',
                    'location': {
                        'latitude': 55.776685,
                        'longitude': 49.116505
                    }
                },
                'delivery_status': 'in_progress',
            },
            {
                'id': 4,
                'delivery_period': {
                    'start': '2018-12-25 12:20:00',
                    'end': '2018-01-25 10:10:00'
                },
                'priority': 242,
                'address_from': {
                    'address': 'ул. Рихарда Зорге, Казань, Респ. Татарстан, 420101',
                    'location': {
                        'latitude': 55.760942,
                        'longitude': 49.189924
                    }
                },
                'address_to': {
                    'address': 'Профсоюзная ул., 8, Казань, Респ. Татарстан, 420111',
                    'location': {
                        'latitude': 55.793669,
                        'longitude': 49.110707
                    }
                },
                'delivery_status': 'in_progress',
            }
        ]

        corders = pending_orders if status == 'pending' else current_orders

        return {
            'total_count': len(corders),
            'results': corders
        }

    def format_pagination(self, request):
        limit = request.query_params.get('limit', None)
        offset = request.query_params.get('offset', 0)

        return limit, offset

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        return Response(self.extract_orders_list(1, 'pending', self.format_pagination(request)), status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def current(self, request):
        return Response(self.extract_orders_list(1, 'in_progress', self.format_pagination(request)), status=HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='pending-orders', permission_classes=[IsAuthenticated])
    def pending_orders(self, request, pk=None):
        return Response(self.extract_orders_list(1, 'pending', self.format_pagination(request)), status=HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='current-orders', permission_classes=[IsAuthenticated])
    def current_orders(self, request, pk=None):
        return Response(self.extract_orders_list(1, 'in_progress', self.format_pagination(request)), status=HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='co-contact', permission_classes=[IsAuthenticated])
    def co_contact(self, request, pk=None):
        try:
            driver = DeliveryOperator.objects.get(pk=pk)
        except DeliveryOperator.DoesNotExist:
            return Response({'msg': 'Driver is not found'}, HTTP_400_BAD_REQUEST)
        control_operators = UserRole.objects.filter(role=AcmeRoles.CO.value)
        control_operators_in_region = []
        for operator in control_operators:
            if operator.user.region == driver.operator.region:
                control_operators_in_region.append(operator)
        if len(control_operators_in_region) == 0:
            return Response({'msg': ('No operators for this region(' + str(driver.operator.region) + ')')},
                            HTTP_400_BAD_REQUEST)

        control_operator = random.choice(control_operators_in_region)  # type: UserRole
        control_operator = control_operator.user
        serializer = AcmeUserSerializer(control_operator)
        return Response(serializer.data,
                        status=HTTP_200_OK)
        return Response({
            'id': 1243,
            'contacts': {
                'first_name': 'Johnathan',
                'last_name': 'Morrison',
                'phone_number': '+1123412341234'
            }
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='location', permission_classes=[IsAuthenticated])
    def get_location(self, request):
        return Response(status=HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='location', permission_classes=[IsAuthenticated])
    def set_location(self, request, pk=None):
        return Response({
            'id': 123,
            'location': {
                'latitude': 123.312,
                'longitude': 321.234,
            },
            'location_updated_at': '1970-01-01 10:10:10',
        }, status=HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request):

        drivers = DeliveryOperator.objects.all()
        drivers_serialized = []

        for driver in drivers:
            serializer = AcmeDeliveryOperatorSerializer(driver)
            temp_result = json.dumps(serializer.data['operator'])
            temp_result = temp_result[:-1]
            temp_result += ','
            temp_location = json.dumps({'location': serializer.data['location']})
            temp_location = temp_location[1:-1]
            temp_result += temp_location + ','

            temp_assigned_count = json.dumps({'assigned_orders_count': serializer.data['assigned_orders_count']})
            temp_assigned_count = temp_assigned_count[1:-1]
            temp_result += temp_assigned_count + ','

            temp_in_progress_count = json.dumps(
                {'in_progress_orders_count': serializer.data['in_progress_orders_count']})
            temp_in_progress_count = temp_in_progress_count[1:-1]
            temp_result += temp_in_progress_count
            temp_result += '}'

            temp_result = json.loads(temp_result)

            drivers_serialized.append(temp_result)

        return Response({
            'total_count': len(drivers_serialized),
            'results': drivers_serialized
        },
            status=HTTP_200_OK)

    @action(detail=True, methods=['GET'],
            permission_classes=[IsAuthenticated])  # todo Change permission Class to  IsControlOperator
    def info(self, request, pk=None):
        try:
            driver = DeliveryOperator.objects.get(pk=pk)
        except DeliveryOperator.DoesNotExist:
            return Response({'msg': 'Driver is not found'}, HTTP_400_BAD_REQUEST)

        serializer = AcmeDeliveryOperatorSerializer(driver)
        temp_result = json.dumps(serializer.data['operator'])
        temp_result = temp_result[:-1]
        temp_result += ','
        temp_location = json.dumps({'location': serializer.data['location']})
        temp_location = temp_location[1:-1]
        temp_result += temp_location + ','

        temp_assigned_count = json.dumps({'assigned_orders_count': serializer.data['assigned_orders_count']})
        temp_assigned_count = temp_assigned_count[1:-1]
        temp_result += temp_assigned_count + ','

        temp_in_progress_count = json.dumps(
            {'in_progress_orders_count': serializer.data['in_progress_orders_count']})
        temp_in_progress_count = temp_in_progress_count[1:-1]
        temp_result += temp_in_progress_count
        temp_result += '}'
        temp_result = json.loads(temp_result)
        return Response(temp_result,
                        status=HTTP_200_OK)
