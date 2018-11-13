from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from web_app.serializers import *

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
            except:
                return Response('', status=HTTP_200_OK)

        elif request.method == 'POST':
            serializer = AcmeOrderStatusCreateSerializer2(data=request.data)
            if serializer.is_valid():
                serializer.save(order_id=pk)
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def delivery_status(self, request, pk=None):
        try:
            order_delivery = OrderDelivery.objects.filter(order__id=pk).order_by('-id')[0]

            serializer = self.get_serializer(order_delivery, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=HTTP_200_OK)

        except:
            return Response('', status=HTTP_200_OK)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request, pk=None):
        '''
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
                'avatar': 'https://backend.acme-company.site/static/uploads/ava1.jpg',
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
        '''

        try:
            order = AcmeOrder.objects.get(pk=pk)
        except DeliveryOperator.DoesNotExist:
            return Response({'msg': 'Order is not found'}, HTTP_400_BAD_REQUEST)

        serializer = AcmeOrderSerializer2(order)
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
            return Response(LocationSerializer2(self.get_location(order)).data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'msg': 'Order or its status were not found'}, HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def assign(self, request):
        try:
            order_id = request.POST['order_id']
            driver_id = request.POST['driver_id']
            end_location_id = request.POST['end_location_id']
            if OrderDelivery.objects.filter(order=order_id, delivery_status='in_progress').count() > 0:
                return Response({'msg': 'Driver is already assigned and delivering this order'},
                                status=HTTP_400_BAD_REQUEST)
            location = self.get_location(AcmeOrder.objects.get(pk=order_id))
            delivery = OrderDelivery(order_id=order_id, delivery_operator_id=driver_id,
                                     delivery_status='pending', start_location_id=location.id,
                                     end_location_id=end_location_id, active_time_period='{[]}')
            delivery.save()
            return Response(AcmeOrderDeliverySerializer2(delivery).data, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg': str(e)}, status=HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list(self, request, pk=None):

        objects = AcmeOrder.objects.all()
        serialized_array = []
        for obj in objects:
            serializer = AcmeOrderSerializer2(obj)
            serialized_array.append(serializer.data)
        print(serialized_array)
        return Response({'result': serialized_array[-1]}, status=HTTP_200_OK)
