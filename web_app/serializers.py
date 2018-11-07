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


class AcmeOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcmeOrder
        fields = '__all__'
