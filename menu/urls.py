from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import MenuItemViews,menuItem
urlpatterns = [
    path('menu-list/',MenuItemViews.as_view(), name='register'),
    path('menu-item/<int:p_id>/',menuItem.as_view(), name='menu item'),
    path('menu-list/<int:p_id>/',MenuItemViews.as_view(), name='update'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)