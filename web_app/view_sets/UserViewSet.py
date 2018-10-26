from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response


class UserViewSet(viewsets.ViewSet):
    def login(self, request):
        print(request)
        print(request.data)

        return Response({'token': 'dsfsdsdffsdsfd'})

    def logout(self, request):
        return Response({})
