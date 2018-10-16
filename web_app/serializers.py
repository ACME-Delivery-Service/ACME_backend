from rest_framework import serializers
from .models import *


class parcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        # fields = ('weight', 'volume', 'shape')
        fields = '__all__'
