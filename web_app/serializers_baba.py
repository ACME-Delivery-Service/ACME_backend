from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ModelField, SerializerMethodField

from .models import *


class ContactSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = 'phone_number'


class AcmeCustomerSerializer2(serializers.ModelSerializer):
    contact = ContactSerializer2()

    class Meta:
        model = AcmeCustomer
        fields = '__all__'


class AcmeOrderStatusSerializer2(serializers.ModelSerializer):
    class Meta:
        model = AcmeOrderStatus
        fields = ['status', ]


class AcmeOrderStatusCreateSerializer2(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['status'] == 'stored' and 'warehouse' not in attrs:
            raise ValidationError({'warehouse': ['Warehouse is required.', ]})
        return attrs

    class Meta:
        model = AcmeOrderStatus
        fields = ['status', 'warehouse', ]


class LocationSerializer2(serializers.ModelSerializer):
    location = SerializerMethodField()

    def get_location(self, obj):
        return {'latitude': obj.latitude, 'longitude': obj.longitude}

    class Meta:
        model = Location
        fields = ['address', 'location', ]


class AcmeUserSerializer2(serializers.ModelSerializer):
    contact = ContactSerializer2()

    class Meta:
        model = AcmeUser
        fields = '__all__'


class AcmeDeliveryOperatorSerializer2(serializers.ModelSerializer):
    avatar_url = SerializerMethodField()

    contacts = SerializerMethodField()

    def get_avatar_url(self, obj):
        return obj.operator.avatar_url

    def get_contacts(self, obj):
        return ContactSerializer2(obj.operator.contact).data

    class Meta:
        model = DeliveryOperator
        fields = ['id', 'avatar_url', 'contacts', ]


class OrderDeliveryCreateSerializer2(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        fields = ['delivery_status', ]


class OrderDeliverySerializer2(serializers.ModelSerializer):
    delivery_operator = AcmeDeliveryOperatorSerializer2()

    class Meta:
        model = OrderDelivery
        fields = ['delivery_operator', ]


class AcmeOrderSerializer2(serializers.ModelSerializer):
    delivery_period = SerializerMethodField()
    address_to = LocationSerializer2(source='end_location')
    address_from = LocationSerializer2(source='start_location')
    status = SerializerMethodField()
    is_assigned = SerializerMethodField()
    delivery_operator = SerializerMethodField()

    def get_delivery_operator(self, obj):
        try:
            return AcmeDeliveryOperatorSerializer2(
                [od.delivery_operator for od in obj.order_deliveries.all()], many=True).data
        except:
            return None

    def get_status(self, obj):
        try:
            return obj.order_status.order_by('-created_on')[0].status
        except:
            return None

    def get_is_assigned(self, obj):
        return self.get_status(obj) in ['pending', 'in_progress', 'en_route']

    def get_delivery_period(self, obj):
        return {'start': obj.scheduled_time_start_time, 'end': obj.scheduled_time_end_time}

    class Meta:
        model = AcmeOrder
        fields = ['id', 'delivery_period', 'priority', 'address_to', 'address_from', 'status', 'is_assigned',
                  'delivery_operator', ]


class AcmeOrderDeliverySerializer2(serializers.ModelSerializer):
    order = AcmeOrderSerializer2()
    delivery_operator = AcmeDeliveryOperatorSerializer2()
    start_location = LocationSerializer2()
    end_location = LocationSerializer2()

    class Meta:
        model = OrderDelivery
        fields = '__all__'
