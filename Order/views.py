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
            msg = "Order(s) Successfully " if isinstance(data, list) else "Order Successfully"
            return Response({"result": serializer.data, "msg": msg}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        # Delete all cart items
        try:
            Order.objects.all().delete()
            msg = "All order items deleted successfully"
            return Response({"msg": msg}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            msg = "Failed to delete all order items"
            return Response({"msg": msg, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk):
        order = self.get_object(pk)
        if order is not None:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        try:
            i_id = int(pk)  # Assuming 'pk' is either the user ID or food ID passed in the URL


            # Check if 'pk' is a valid user ID
            if Order.objects.filter(account_id=i_id).exists():
                orders = Order.objects.filter(account_id=i_id)

                # Update all orders for the user
                for order in orders:
                    order.completed = True
                    order.save()
                return Response({"message": "All orders updated successfully!"})

            # Check if 'pk' is a valid food ID
            elif Order.objects.filter(id=i_id).exists():
                # Update the specific order by setting 'completed' to True
                order = Order.objects.get(id=i_id)
                order.completed = True
                order.save()
                return Response({"message": "Order updated successfully!"})

            return Response({'error': 'Invalid user ID or food ID'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid ID format'}, status=status.HTTP_400_BAD_REQUEST)

   

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order is not None:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

# not completed data for the user
class NotCompletedOrder(APIView):
    def get(self, request, pk):
        try:
            orders = Order.objects.filter(account_id=pk, completed=False)
            serializer = OrderSerializer(orders, many=True)
            for order_data in serializer.data:
                order = Order.objects.get(id=order_data['id'])
                order_data['account'] = UserSerializer(order.account).data
                order_data['menu_item'] = MenuItemSerializer(order.menu_item).data
        
            return Response({"result":serializer.data},status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#  completed data for the user
class CompletedOrder(APIView):
    def get(self, request, pk):
        try:
            orders = Order.objects.filter(account_id=pk, completed=True)
            serializer = OrderSerializer(orders, many=True)
            for order_data in serializer.data:
                order = Order.objects.get(id=order_data['id'])
                order_data['account'] = UserSerializer(order.account).data
                order_data['menu_item'] = MenuItemSerializer(order.menu_item).data
        
            return Response({"result":serializer.data},status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# cart data 

# This CarViewset is not use for now
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartListCreateAPIView(APIView):
    def calculate_grand_total(self, cart):
        return sum(item.totalPrice for item in cart.f_id.cart_set.all())

    def get(self, request):
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        for cart_data in serializer.data:
            cart = Cart.objects.get(id=cart_data['id'])
            cart_data['u_id'] = UserSerializer(cart.u_id).data
            cart_data['f_id'] = MenuItemSerializer(cart.f_id).data
            grand_total = self.calculate_grand_total(cart)  # Calculate grand total for each cart
            cart_data['grand_total'] = grand_total
        
        
        return Response({"result":serializer.data},status=status.HTTP_200_OK)
    def post(self, request):
        
            # Handle single item order
        serializer = CartSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            msg = "successful"
            return Response({"result": serializer.data, "msg": msg}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        # Delete all cart items
        try:
            Cart.objects.all().delete()
            msg = "All cart items deleted successfully"
            return Response({"msg": msg}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            msg = "Failed to delete all cart items"
            return Response({"msg": msg, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
class CartDetailApiView(APIView):
    def get_object(self, pk):
        try:
            return Cart.objects.get(id=pk)
        except Cart.DoesNotExist:
            return None


    def get(self, request, pk):
        cart = self.get_object(pk)
        if cart is not None:
            serializer = CartSerializer(cart)
         
           
            return Response( serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        pk = int(pk)
        try:
            item = Cart.objects.get(id=pk)
        except Cart.DoesNotExist:
            return Response({'error': 'cart not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartSerializer(instance=item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Item updated successfully!", 'result': serializer.data})
        
        return Response({"error": serializer.errors, "message": "Order Update failed."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart = self.get_object(pk)
        if cart is not None:
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)