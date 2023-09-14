from django.urls import path


from .views import MenuItemViews,menuItem
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MenuItemViewSet,VegFoodCategoryAPIView,CategoryListAPIView



urlpatterns = [
    path('menu-list/',MenuItemViews.as_view(), name='register'),
    path('menu-item/<int:p_id>/',menuItem.as_view(), name='menu item'),
    path('menu-list/<int:p_id>/',MenuItemViews.as_view(), name='update'),
    path('veg-menu-list/<str:veg>/',VegFoodCategoryAPIView.as_view(), name='veg-item'),
    path('category/',CategoryListAPIView.as_view(), name='category-list'),
    path('category/<str:category>',CategoryListAPIView.as_view(), name='category-list'),


]
router = DefaultRouter()
router.register(r'menuitems', MenuItemViewSet)

urlpatterns += [
    path('', include(router.urls)),
]

