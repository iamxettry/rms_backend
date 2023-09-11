# urls.py in each app
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,CartViewSet
from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView,CartListCreateAPIView,CartDetailApiView,NotCompletedOrder,CompletedOrder

# OrderViewSet is not used here
router = DefaultRouter()
router.register(r'orders1', OrderViewSet)
router.register(r'cart1', CartViewSet)

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('not-completed-orders/<int:pk>/', NotCompletedOrder.as_view(), name='not-completed-order'),
    path('completed-orders/<int:pk>/', CompletedOrder.as_view(), name='completed-order'),
    path('cart/', CartListCreateAPIView.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartDetailApiView.as_view(), name='cart-detail'),

]

urlpatterns += router.urls  #not used for now
