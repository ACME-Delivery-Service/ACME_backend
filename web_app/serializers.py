from rest_framework import serializers
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
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AcmeOrderSerializer(serializers.ModelSerializer):
    customer = AcmeCustomerSerializer()
    start_location = LocationSerializer()
    end_location = LocationSerializer()

    class Meta:
        model = AcmeOrder
        fields = '__all__'


class AcmeUserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer()

    class Meta:
        model = AcmeUser
        fields = ('id', 'avatar', 'contacts')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AcmeDeliveryOperatorSerializer(serializers.ModelSerializer):
    operator = AcmeUserSerializer()
    location = LocationSerializer()
    assigned_orders_count = serializers.SerializerMethodField('assigned_count')
    in_progress_orders_count = serializers.SerializerMethodField('in_progress_count')

    def in_progress_count(self, obj: DeliveryOperator):
        orders = OrderDelivery.objects.all()
        count = 0

        for order in orders:
            if obj.id == order.delivery_operator_id and order.delivery_status == 'in_progress':
                count += 1
        return count

    def assigned_count(self, obj: DeliveryOperator):
        orders = OrderDelivery.objects.all()
        count = 0

        for order in orders:
            if obj.id == order.delivery_operator_id:
                count += 1
        return count

    class Meta:
        model = DeliveryOperator
        fields = ('operator', 'assigned_orders_count', 'in_progress_orders_count', 'location')


class AcmeOrderDeliverySerializer(serializers.ModelSerializer):
    order = AcmeOrderSerializer()
    delivery_operator = AcmeDeliveryOperatorSerializer()
    start_location = LocationSerializer()
    end_location = LocationSerializer()

    class Meta:
        model = OrderDelivery
        fields = '__all__'
