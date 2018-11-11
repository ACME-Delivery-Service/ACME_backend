from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from web_app.serializers import *

from web_app.models import AcmeOrder, Location, AcmeOrderStatus, OrderDelivery
import json


class OrderViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == 'status':
            return AcmeOrderStatusSerializer()
        return AcmeOrderSerializer()

    @action(detail=False, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def status(self, request, pk=None):

        if request.method == 'GET':
            status = get_object_or_404(AcmeOrderStatus.objects.all(), order_id__id=pk)

            return Response(self.get_serializer(status), status=HTTP_200_OK)

        elif request.method == 'POST':
            serializer = AcmeOrderStatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=self.status.HTTP_201_CREATED)
            return Response(serializer.errors, status=self.status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        try:
            order = AcmeOrder.objects.get(pk=pk)
        except DeliveryOperator.DoesNotExist:
            return Response({'msg': 'Order is not found'}, HTTP_400_BAD_REQUEST)

        serializer = AcmeOrderSerializer(order)
        return Response(serializer.data,
                        status=HTTP_200_OK)

    def get_location(self, order):
        location = Location.objects.first()
        status = AcmeOrderStatus.objects.filter(order_id=order.id).order_by('created_on').last()
        if status.status == 'created' or status.status == 'approved':
            location = order.start_location
        elif status.status == 'en_route':
            delivery = OrderDelivery.objects.filter(order=order.id, delivery_status='in_progress').first()
            location = delivery.delivery_operator.current_location
        elif status.status == 'stored':
            warehouse = Warehouse.objects.get(pk=status.warehouse_id)
            location = Location.objects.first()
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

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def assign(self, request):
        try:
            order_id = request.POST['order_id']
            driver_id = request.POST['driver_id']
            end_location_id = request.POST['end_location_id']
            if OrderDelivery.objects.filter(order=order_id, delivery_status='in_progress').count() > 0:
                return Response({'msg': 'Driver is already assigned and delivering this order'}, status=HTTP_400_BAD_REQUEST)
            location = self.get_location(AcmeOrder.objects.get(pk=order_id))
            delivery = OrderDelivery(order_id=order_id, delivery_operator_id=driver_id,
                                     delivery_status='pending', start_location_id=location.id,
                                     end_location_id=end_location_id, active_time_period='{[]}')
            delivery.save()
            return Response(AcmeOrderDeliverySerializer(delivery).data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': str(e)}, status=HTTP_400_BAD_REQUEST)

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
