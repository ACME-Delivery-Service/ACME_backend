from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class parcelList(APIView):

    def get(self, request):
        parcel1 = Parcel.objects.all()
        serializer = parcelSerializer(parcel1, many=True)
        return Response(serializer.data)

    def post(self):
        pass

