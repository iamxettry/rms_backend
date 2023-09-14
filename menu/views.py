from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from .serializers import MenuItemSerializer
from rest_framework.views import APIView
from .models import Menuitem
from .serializers import MenuItemSerializer


from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

class MenuItemViews(APIView):
    def post(self, request):
        serializer=MenuItemSerializer(data=request.data)
        print(serializer)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"menudata":serializer.data,"message": "Menu Created Successfully."},status=status.HTTP_201_CREATED, content_type="application/json")

        return Response({"error":serializer.errors,"message": "Menu creation failed."}, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
    

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
        return Response(data,status=status.HTTP_200_OK)
    
    def put(self,request,p_id):
        p_id=int(p_id)
        try:
            item_shelf =Menuitem.objects.get(id=p_id)
            print(item_shelf)
        except Menuitem.DoesNotExist:
            return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer=MenuItemSerializer( instance=item_shelf,data=request.data)
        print("edit item",serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"Menu updated successfully!",'result':serializer.data},content_type="application/json")
        return Response({"error":serializer.errors,"message": "Menu Update failed."}, status=status.HTTP_400_BAD_REQUEST,content_type="application/json")
    
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

# views.py


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = Menuitem.objects.all()
    serializer_class = MenuItemSerializer
    parser_classes = (MultiPartParser, FormParser)
    def create(self, request, *args, **kwargs):
        name=request.data['name']
        category=request.data['category']
        price=request.data['price']
        itemtype=request.data['itemtype']
        img=request.data['img']
        available=request.data['available']
        calorie=request.data['calorie']
        Menuitem.objects.create(name=name,category=category,price=price,itemtype=itemtype,img=img,available=available,calorie=calorie)
        return Response("Menu created successfully",status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Menuitem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)



# filtered data based on type veg

class VegFoodCategoryAPIView(APIView):
    def get(self, request, veg):
        is_vegetarian = veg.lower() == 'veg'
        # Filter food items based on whether they are vegetarian or non-vegetarian
        food_items = Menuitem.objects.filter(itemtype=is_vegetarian)
     

        # Serialize the filtered food items
        serializer = MenuItemSerializer(food_items, many=True)
        for item in serializer.data:
            item['img'] = request.build_absolute_uri(item['img'])

        # Return the serialized data as a JSON response
        return Response({"msg":"Success","result":serializer.data}, status=status.HTTP_200_OK) 


# filtered data based on category
class CategoryListAPIView(APIView):
      def get(self, request, category=None):
        if category is None:
            # No category provided, list all categories
            categories = Menuitem.objects.values('category').distinct()
            result = []
            for cat in categories:
                category_name = cat['category']
                
                # Retrieve all items for the current category
                items = Menuitem.objects.filter(category=category_name)
                
                # Serialize the items for the category
                serialized_items = MenuItemSerializer(items, many=True).data
                # Build image URLs for each item in the category
                for item in serialized_items:
                    item['img'] = request.build_absolute_uri(item['img'])

                
                # Add the category and its items to the result list
                result.append({
                    "category": category_name,
                    "data": serialized_items
                })
            
            return Response({"result": result}, status=status.HTTP_200_OK)
        else:
            # Filter food items based on the provided category
            food_items = Menuitem.objects.filter(category=category)

            # Serialize the filtered food items
            serializer = MenuItemSerializer(food_items, many=True)
            for item in serializer.data:
                item['img'] = request.build_absolute_uri(item['img'])

            # Return the serialized data as a JSON response
            return Response({"msg": "Success", "result": [{"category": category, "data": serializer.data}]}, status=status.HTTP_200_OK)