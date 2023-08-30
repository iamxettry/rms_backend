from rest_framework import serializers
from .models import accountUser


# user registration serializer
class RegisterSerializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, style={'input_type':'password'})
    class Meta:
        model=accountUser
        fields=['email','username','password']


    def create(self, validated_data):
        return accountUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


# user login serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # username=serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})   


#user profile serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountUser
        fields = ['id', 'username', 'email']