from rest_framework import serializers
from .models import accountUser

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from account.utils import Util
from django.core.mail import send_mail

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
        fields = ['id', 'username', 'email','is_superuser']




class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if accountUser.objects.filter(email=email).exists():
      user = accountUser.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = f'http://localhost:3000/auth/reset-password/{uid}/{token}'
      print('Password Reset Link', link)
      # Send EMail
      body = f'Click Following Link to Reset Your Password {link}'
    #   send_mail(
    #     'Password Reset',
    #     body,
    #     'rajuchhetri7112@gmail.com',
    #     [email],
    #     fail_silently=False,
    #         )
    
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
  newPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['newPassword', 'confPassword']

  def validate(self, attrs):
    try:
      newPassword = attrs.get('newPassword')
      confPassword = attrs.get('confPassword')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if newPassword != confPassword:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = accountUser.objects.get(id=id)
      print(user)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(newPassword)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')