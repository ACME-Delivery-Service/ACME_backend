from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from web_app.exceptions import AcmeAPIException
from web_app.permissions import IsAuthenticatedOrMeta
from web_app.serializers_baba import *


class CustomerViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticatedOrMeta])
    def info(self, request, pk=None):
        try:
            customer = AcmeCustomer.objects.get(pk=pk)
        except AcmeCustomer.DoesNotExist:
            raise AcmeAPIException('Customer not found')
        else:
            return Response(AcmeCustomerSerializer2(customer).data, status=HTTP_200_OK)
