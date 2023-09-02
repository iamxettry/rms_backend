from rest_framework import serializers
from .models import Menuitem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menuitem
        fields='__all__'