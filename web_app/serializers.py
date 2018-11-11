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
    contact = ContactSerializer()

    class Meta:
        model = AcmeUser
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AcmeDeliveryOperatorSerializer(serializers.ModelSerializer):
    operator = AcmeUserSerializer()
    current_location = LocationSerializer()

    class Meta:
        model = DeliveryOperator
        fields = '__all__'


class AcmeOrderDeliverySerializer(serializers.ModelSerializer):
    order = AcmeOrderSerializer()
    delivery_operator = AcmeDeliveryOperatorSerializer()
    start_location = LocationSerializer()
    end_location = LocationSerializer()
    class Meta:
        model = OrderDelivery
        fields = '__all__'
