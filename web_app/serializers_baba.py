from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ModelField, SerializerMethodField

from .models import *


class ContactSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


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
    class Meta:
        model = Location
        fields = '__all__'


class AcmeUserSerializer2(serializers.ModelSerializer):
    contact = ContactSerializer2()

    class Meta:
        model = AcmeUser
        fields = '__all__'


class AcmeDeliveryOperatorSerializer2(serializers.ModelSerializer):
    avatar = SerializerMethodField()

    contacts = SerializerMethodField()

    # current_location = LocationSerializer()

    def get_avatar(self, obj):
        return obj.operator.avatar

    def get_contacts(self, obj):
        return ContactSerializer2(obj.operator.contact).data

    class Meta:
        model = DeliveryOperator
        fields = ['id', 'avatar', 'contacts', ]


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
    start_location = LocationSerializer2()
    end_location = LocationSerializer2()
    operators = SerializerMethodField()
    status = SerializerMethodField()
    is_assigned = SerializerMethodField()

    def get_operators(self, obj):
        return AcmeDeliveryOperatorSerializer2(
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


class AcmeOrderDeliverySerializer2(serializers.ModelSerializer):
    order = AcmeOrderSerializer2()
    delivery_operator = AcmeDeliveryOperatorSerializer2()
    start_location = LocationSerializer2()
    end_location = LocationSerializer2()

    class Meta:
        model = OrderDelivery
        fields = '__all__'
