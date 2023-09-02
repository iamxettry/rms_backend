from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializers import MenuItemSerializer
from rest_framework.views import APIView
from .models import Menuitem
from .serializers import MenuItemSerializer

class MenuItemViews(APIView):
    def post(self, request):
        serializer=MenuItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"menudata":serializer.data,"message": "Menu Created Successfully."},status=status.HTTP_201_CREATED)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        queryset = Menuitem.objects.all()
        serializer = MenuItemSerializer(queryset, many=True)
        count=queryset.count()
        data = {
            "status": "success",
            "url": request.build_absolute_uri(),
            "result": serializer.data,
            "count":count
        }
        return Response(data)
    
    def put(self,request,p_id):
        p_id=int(p_id)
        try:
            item_shelf =Menuitem.objects.get(id=p_id)
        except Menuitem.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=MenuItemSerializer( instance=item_shelf,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Menu updated successfully!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class menuItem(APIView):
    def get(self, request,p_id):
        p_id=int(p_id)
        try:
            instance = Menuitem.objects.get(id=p_id)  # Use 'id' or the correct field name
            serializer = MenuItemSerializer(instance)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Menuitem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, p_id):
        try:
            item = Menuitem.objects.get(id=p_id)
            item.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Menuitem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)