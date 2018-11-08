from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from web_app.serializers import *

from web_app.models import AcmeOrder, Location, Parcel, AcmeCustomer, Contact, AcmeOrderStatus
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
            start_location = Location.objects.get(pk=order.start_location_id)
            end_location = Location.objects.get(pk=order.end_location_id)
            parcels = Parcel.objects.filter(order_id=pk)
            customer = AcmeCustomer.objects.get(pk=order.customer_id)
            customer_contact = Contact.objects.get(pk=customer.pk)
            order_statuses = AcmeOrderStatus.objects.filter(order_id=order.pk)
            current_status = order_statuses.order_by('created_on').last()
            status = "None"
            if current_status != None:
                status = current_status.status
            parcels_info = []
            for parcel in parcels:
                parcel_info = {
                        'id': parcel.pk,
                        'weight': parcel.weight,
                        'dimensions': {
                            'x': parcel.dimension[0],
                            'y': parcel.dimension[1],
                            'z': parcel.dimension[2],
                        },
                        'shape': parcel.shape,
                        'description': "No description provided."
                    }
                parcels_info.append(parcel_info)
            return Response({
                'id': pk,
                'delivery_period': {
                    'start': order.scheduled_time.start_time,
                    'end': order.scheduled_time.end_time
                },
                'priority': order.priority,
                'address_from': {
                    'address': start_location.location_address,
                    'location': {
                        'latitude': start_location.lat_long.x,
                        'longitude': start_location.lat_long.y
                    }
                },
                'address_to': {
                    'address': end_location.location_address,
                    'location': {
                        'latitude': end_location.lat_long.x,
                        'longitude': end_location.lat_long.y
                    }
                },
                'description': order.comment,
                'parcels_info': parcels_info,
                'customer_info': {
                    'id': customer.pk,
                    'contacts': {
                        'first_name': customer_contact.first_name,
                        'last_name': customer_contact.last_name,
                        'phone_number': customer_contact.phone_number
                    },
                },
                'status': status
            }, status=HTTP_200_OK)
        except AcmeOrder.DoesNotExist:
            return Response({'msg': 'No ID provided'}, HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def location(self, request, pk=None):
        order = AcmeOrder.objects.get(pk=pk)
        location = Location.objects.get(pk=order.start_location_id)
        return Response({
            'id': location.pk,
            'location': {
                'latitude': location.lat_long.x,
                'longitude': location.lat_long.y
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
