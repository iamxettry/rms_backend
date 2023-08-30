from django.urls import path
from .views import RegisterView,UserLoginView,userProfile
urlpatterns = [
    path('signup/',RegisterView.as_view(), name='register'),
    path('login/',UserLoginView.as_view(), name='login'),
    path('profile/',userProfile.as_view(), name='profile')
]