from django.urls import path


from .views import MenuItemViews,menuItem
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet,FoodCategoryAPIView,VegFoodCategoryAPIView



urlpatterns = [
    path('menu-list/',MenuItemViews.as_view(), name='register'),
    path('menu-item/<int:p_id>/',menuItem.as_view(), name='menu item'),
    path('menu-list/<int:p_id>/',MenuItemViews.as_view(), name='update'),
    path('filtered-menu-list/<str:category>/',FoodCategoryAPIView.as_view(), name='filtered-items'),
    path('veg-menu-list/<str:veg>/',VegFoodCategoryAPIView.as_view(), name='veg-item'),


]
router = DefaultRouter()
router.register(r'menuitems', MenuItemViewSet)

urlpatterns += [
    path('', include(router.urls)),
]

