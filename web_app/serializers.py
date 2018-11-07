from rest_framework import serializers
from .models import *


class parcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'


class AcmeCustomer(serializers.ModelSerializer):
    class Meta:
        model = AcmeCustomer
        fields = '__all__'


class Contact(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class AcmeOrderStatus(serializers.ModelSerializer):
    class Meta:
        model = AcmeOrderStatus
        fields = '__all__'


class AcmeOrder(serializers.ModelSerializer):
    class Meta:
        model = AcmeOrder
        fields = '__all__'
