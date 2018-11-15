from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from web_app.exceptions import AcmeAPIException
from web_app.serializers_baba import *
from web_app.serializers_default import *
from django.db.models import Q

from web_app.models import AcmeOrder, Location, AcmeOrderStatus, OrderDelivery


class OrderViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'status':
            return AcmeOrderStatusSerializer2
        elif self.action == 'delivery_status':
            return OrderDeliveryCreateSerializer2
        return AcmeOrderSerializer2

    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def status(self, request, pk=None):
        if request.method == 'GET':
            try:
                status = AcmeOrderStatus.objects.filter(order__id=pk).order_by('-created_on')[0]
                return Response(status.status, status=HTTP_200_OK)
            except AcmeOrderStatus.DoesNotExist:
                raise AcmeAPIException('Order not found')

        elif request.method == 'POST':
            try:
                order_status = AcmeOrderStatus.objects.get(pk=pk)
                if not order_status:
                    raise AcmeAPIException('Order not found')

                new_status = request.data.get('status')
                order_status.status = new_status
                order_status.save()

                return Response(status=HTTP_200_OK)
            except AcmeOrderStatus.DoesNotExist:
                raise AcmeAPIException('Order don\'t have status')

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def delivery_status(self, request, pk=None):
        try:
            order_delivery = OrderDelivery.objects.filter(order__id=pk).order_by('-id')[0]
            if not order_delivery:
                raise AcmeAPIException('Order not found')

            new_status = request.data.get('status')
            order_delivery.delivery_status = new_status
            order_delivery.save()

            return Response(status=HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        try:
            order = AcmeOrder.objects.get(pk=pk)
        except DeliveryOperator.DoesNotExist:
            raise AcmeAPIException('Order not found')

        serializer = AcmeOrderSerializer(order)
        return Response(serializer.data, status=HTTP_200_OK)

    def get_location(self, order):
        location = Location.objects.first()
        status = AcmeOrderStatus.objects.filter(order_id=order.id).order_by('created_on').last()
        if status.status == 'created' or status.status == 'approved':
            location = order.start_location
        elif status.status == 'en_route':
            delivery = OrderDelivery.objects.filter(order=order.id, delivery_status='in_progress').first()
            location = delivery.delivery_operator.current_location
        elif status.status == 'stored':
            warehouse = status.warehouse
            location = warehouse.location
        elif status.status == 'delivered':
            location = order.end_location
        return location

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def location(self, request, pk=None):
        try:
            order = AcmeOrder.objects.get(pk=pk)
            return Response(LocationSerializer(self.get_location(order)).data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Order or its status were not found'}, HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def assign(self, request, pk=None):
        try:
            order_id = pk
            driver_id = request.POST['driver_id']
            try:
                order = AcmeOrder.objects.get(pk=order_id)
            except DeliveryOperator.DoesNotExist:
                return Response({'msg': 'Order not found'}, HTTP_400_BAD_REQUEST)
            try:
                driver = DeliveryOperator.objects.get(pk=driver_id)
            except DeliveryOperator.DoesNotExist:
                return Response({'msg': 'Delivery operator not found'}, HTTP_400_BAD_REQUEST)
            end_location_id = request.POST['end_location_id']
            if OrderDelivery.objects.filter(Q(delivery_status='in_progress') | Q(delivery_status='pending'),
                                            order=order_id).count() > 0:
                return Response({'msg': 'Driver is already assigned and delivering this order'},
                                status=HTTP_400_BAD_REQUEST)
            location = self.get_location(AcmeOrder.objects.get(pk=order_id))
            delivery = OrderDelivery(order_id=order_id, delivery_operator_id=driver_id,
                                     delivery_status='pending', start_location_id=location.id,
                                     end_location_id=end_location_id, active_time_period=list())
            delivery.save()
            return Response(AcmeOrderDeliverySerializer(delivery).data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg': str(e)}, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request, pk=None):

        objects = AcmeOrder.objects.all()
        serialized_array = []
        for obj in objects:
            serializer = AcmeOrderSerializer2(obj)
            serialized_array.append(serializer.data)

        return Response({
            'total_count': len(serialized_array),
            'results': serialized_array[::-1]
        }, status=HTTP_200_OK)


"""

'''
/orders/list - GET запрос
Требуется авторизация
Имеет пагинацию - можно передать limit и offset, если не заданы, то limit = infinity offset = 0
Возвращает
{
    # 'total_count': 123,
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
        'status': Enum(),
        'is_assigned': true,
        'delivery_operator': {
            'id': 123,
            'avatar': 'http',
            'contacts': {
                'phone_number': '+757488',
            }
        }|null,
    }]
}
'''
"""
