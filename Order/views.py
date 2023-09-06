from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import  Order,Cart
from .serializers import OrderSerializer,CartSerializer

from account.serializers import UserSerializer
from menu.serializers import MenuItemSerializer

# Create your views here.

# --OrderViewSet Is not used for now
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



# used path /orders
class OrderListCreateAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        for order_data in serializer.data:
            order = Order.objects.get(id=order_data['id'])
            order_data['account'] = UserSerializer(order.account).data
            order_data['menu_item'] = MenuItemSerializer(order.menu_item).data
        
        return Response({"result":serializer.data},status=status.HTTP_200_OK)
    def post(self, request):
        # Handle both single and multiple item orders here
        data = request.data
        if isinstance(data, list):
            # Handle multiple item orders
            serializer = OrderSerializer(data=data, many=True)
        else:
            # Handle single item order
            serializer = OrderSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            msg = "Order(s) Successfully Created" if isinstance(data, list) else "Order Successfully Created"
            return Response({"result": serializer.data, "msg": msg}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class OrderDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if order is not None:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        pk=int(pk)
        try:
            item =Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=OrderSerializer( instance=item,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Order updated successfully!",'result':serializer.data})
        return Response({"error":serializer.errors,"message": "Order Update failed."}, status=status.HTTP_400_BAD_REQUEST)
   

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order is not None:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)



# cart data 

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
