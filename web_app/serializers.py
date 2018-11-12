from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ModelField, SerializerMethodField

from .models import *


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class AcmeCustomerSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = AcmeCustomer
        fields = '__all__'


class AcmeOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcmeOrderStatus
        fields = ['status', ]


class AcmeOrderStatusCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['status'] == 'stored' and 'warehouse' not in attrs:
            raise ValidationError({'warehouse': ['Warehouse is required.', ]})
        return attrs

    class Meta:
        model = AcmeOrderStatus
        fields = ['status', 'warehouse', ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AcmeUserSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = AcmeUser
        fields = '__all__'


class AcmeDeliveryOperatorSerializer(serializers.ModelSerializer):
    avatar_url = SerializerMethodField()

    contacts = SerializerMethodField()

    # current_location = LocationSerializer()

    def get_avatar_url(self, obj):
        return obj.operator.avatar_url

    def get_contacts(self, obj):
        return ContactSerializer(obj.operator.contact).data

    class Meta:
        model = DeliveryOperator
        fields = ['id', 'avatar_url', 'contacts', ]


class OrderDeliveryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDelivery
        fields = ['delivery_status', ]


class OrderDeliverySerializer(serializers.ModelSerializer):
    delivery_operator = AcmeDeliveryOperatorSerializer()

    class Meta:
        model = OrderDelivery
        fields = ['delivery_operator', ]


class AcmeOrderSerializer(serializers.ModelSerializer):
    start_location = LocationSerializer()
    end_location = LocationSerializer()
    operators = SerializerMethodField()
    status = SerializerMethodField()
    is_assigned = SerializerMethodField()

    def get_operators(self, obj):
        return AcmeDeliveryOperatorSerializer(
            [od.delivery_operator for od in obj.order_deliveries.all()], many=True).data

    def get_status(self, obj):
        try:
            return obj.order_status.order_by('-created_on')[0].status
        except:
            return None

    def get_is_assigned(self, obj):
        return self.get_status(obj) in ['pending', 'in_progress', 'en_route']
        # return len(OrderDelivery.objects.filter(order=obj)) > 0

    class Meta:
        model = AcmeOrder
        fields = ['priority', 'start_location', 'end_location', 'scheduled_time_start_time',
                  'scheduled_time_end_time', 'operators', 'status', 'is_assigned', ]


class AcmeOrderDeliverySerializer(serializers.ModelSerializer):
    order = AcmeOrderSerializer()
    delivery_operator = AcmeDeliveryOperatorSerializer()
    start_location = LocationSerializer()
    end_location = LocationSerializer()

    class Meta:
        model = OrderDelivery
        fields = '__all__'
