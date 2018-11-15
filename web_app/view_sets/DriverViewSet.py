import json
import random

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from web_app.exceptions import *

from web_app.models import *
from web_app.serializers_default import *


class DriverViewSet(viewsets.ViewSet):

    def extract_orders_list(self, user_id, status, pagination):
        driver = DeliveryOperator.objects.get(operator_id=user_id)
        pending_orders = OrderDelivery.objects.filter(delivery_operator_id=driver.id, delivery_status=status)
        orders = [AcmeOrderDeliverySerializer(order).data for order in pending_orders]

        return {
            'total_count': len(orders),
            'results': orders,
        }

    def format_pagination(self, request):
        limit = request.query_params.get('limit', None)
        offset = request.query_params.get('offset', 0)

        return limit, offset

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def pending(self, request):
        try:
            orders = self.extract_orders_list(request.user.id, 'pending', self.format_pagination(request))
            return Response(orders, status=HTTP_200_OK)
        except Exception as e:
            AcmeAPIException(str(e))

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def current(self, request):
        try:
            orders = self.extract_orders_list(request.user.id, 'in_progress', self.format_pagination(request))
            return Response(orders, status=HTTP_200_OK)
        except Exception as e:
            AcmeAPIException(str(e))

    @action(detail=True, methods=['GET'], url_path='pending-orders', permission_classes=[IsAuthenticated])
    def pending_orders(self, request, pk=None):
        try:
            orders = self.extract_orders_list(pk, 'pending', self.format_pagination(request))
            return Response(orders, status=HTTP_200_OK)
        except Exception as e:
            AcmeAPIException(str(e))

    @action(detail=True, methods=['GET'], url_path='current-orders', permission_classes=[IsAuthenticated])
    def current_orders(self, request, pk=None):
        try:
            orders = self.extract_orders_list(pk, 'in_progress', self.format_pagination(request))
            return Response(orders, status=HTTP_200_OK)
        except Exception as e:
            AcmeAPIException(str(e))

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

    @action(detail=True, methods=['GET', 'POST'], url_path='location', permission_classes=[IsAuthenticated])
    def get_location(self, request, pk=None):
        if request.method == 'GET':
            try:
                location = DeliveryOperator.objects.get(pk=pk).location
                location_json = LocationSerializer(location).data
                location_json['location_updated_at'] = DeliveryOperator.objects.get(pk=pk).location_last_updated
                return Response(location_json, status=HTTP_200_OK)
            except Exception as e:
                return Response(str(e), status=HTTP_400_BAD_REQUEST)
        else:
            try:
                location_info = request.data
                location = Location(latitude=location_info['latitude'], longitude=location_info['longitude'],
                                    address="-")
                location.save()
                operator = DeliveryOperator.objects.get(pk=pk)
                operator.location_id = location.pk
                operator.save()
                return Response(LocationSerializer(location).data, status=HTTP_200_OK)
            except Exception as e:
                return Response(str(e), status=HTTP_400_BAD_REQUEST)

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
