from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserCreationSerializer
from drf_yasg.utils import swagger_auto_schema


class HelloAuthView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello Auth")
    def get(self,request):
        return Response(data={"message":"Hello Auth!"},status = status.HTTP_200_OK)



class UserCreationView(generics.GenericAPIView):
    serializer_class = UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create an Account")
    def post(self,request):
        data = request.data
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data,status = status.HTTP_201_CREATED)
        return Response(data = serializer.errors,status = status.HTTP_400_BAD_REQUEST)
