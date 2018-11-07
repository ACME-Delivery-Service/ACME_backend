from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from web_app.serializers import *


class CustomerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = [IsAuthenticated, ]

    serializer_class = AcmeCustomerSerializer

