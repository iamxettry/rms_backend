from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login
from .serializers import RegisterSerializers,LoginSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import permissions
from account.renderers import UserRenderer
from rest_framework.permissions import AllowAny


#Function to generate the token for the user
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


# views for registration
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format="json"):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"userdata":serializer.data,"message": "User Created Successfully.Now perform Login to get your token"},status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views for login 
class UserLoginView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                # Create or retrieve a token for the user
                token = get_tokens_for_user(user)
                # Return the token and user data
                return Response({'token': token, 'user_id': user.id, 'email': user.email}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

# views for user profile information
class userProfile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)