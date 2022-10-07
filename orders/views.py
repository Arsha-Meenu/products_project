from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import Order
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from drf_yasg.utils import swagger_auto_schema


CustomUser = get_user_model()

class HelloOrderView(generics.GenericAPIView):
    def get(self,request):
        return Response(data={"message":"Hello Order!"},status = status.HTTP_200_OK)


class CreateListOrderView(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.OrderCreationSerializer
    queryset = Order.objects.all()

    @swagger_auto_schema(operation_summary="Get Orders")
    def get(self,request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance = orders,many=True)
        return Response(data = serializer.data,status = status.HTTP_200_OK)

    def post(self,request):
        data = request.data
        print('data',data)
        serializer = self.serializer_class(data = data)
        user = request.user
        print('user',user)
        if serializer.is_valid(raise_exception =True):
            serializer.save(customer = user)
            return Response(data = serializer.data,status= status.HTTP_201_CREATED)
        return Response(data =serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = (IsAdminUser,)

    def get(self,request,order_id):
        order = get_object_or_404(Order,pk = order_id)
        serializers = self.serializer_class(instance = order)
        return Response(data = serializers.data,status = status.HTTP_200_OK)


    def put(self,request,order_id):
        data = request.data
        order = get_object_or_404(Order, pk=order_id)
        serializers = self.serializer_class(instance = order,data=data)
        if serializers.is_valid():
            serializers.save(customer = request.user)
            return Response(data = serializers.data,status = status.HTTP_200_OK)
        return Response(data=serializers.errors,status = status.HTTP_400_BAD_REQUEST)



    def delete(self,request,order_id):
        order = get_object_or_404(Order,pk = order_id)
        order.delete()
        return Response("Order deleted successfully.",status = status.HTTP_204_NO_CONTENT)



class UpdateOrderStatusView(generics.GenericAPIView):
    serializer_class  = serializers.OrderStatusUpdateSerializer

    def put(self,request,order_id):
        order = get_object_or_404(Order,pk = order_id)
        data = request.data
        serializer = self.serializer_class(data = data,instance =order)
        if serializer.is_valid():
            serializer.save()
            return Response(data = serializer.data,status = status.HTTP_200_OK)
        return Response(data =serializer.errors,status = status.HTTP_400_BAD_REQUEST)



class UserOrdersView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer


    def get(self,request,user_id):

        user = CustomUser.objects.filter(pk = user_id).exists()
        if user:
            orders = Order.objects.filter(customer = user ).all()
            serializer =self.serializer_class(instance = orders,many =True)
            return Response(data = serializer.data,status = status.HTTP_200_OK)
        return Response(data = 'User doesnot exist.',status = status.HTTP_204_NO_CONTENT)


class UserOrderDetailsView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    def get(self,request,user_id,order_id):
        user = CustomUser.objects.filter(pk = user_id).exists()
        if user:
            order = Order.objects.filter(customer = user).filter(id =order_id).all()
            serializer = self.serializer_class(instance = order,many = True)
            return Response(data = serializer.data,status=status.HTTP_200_OK)
        return Response(data = "User Doesnot Exists.")