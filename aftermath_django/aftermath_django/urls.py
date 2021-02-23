"""aftermath_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from django.views.generic import TemplateView
from rest_framework import routers

from aftermath_django import settings
from item_management import views

router = routers.DefaultRouter()
router.register(r'armor', views.ArmorViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'itemslots', views.ItemSlotViewSet)
router.register(r'players', views.PlayerViewSet)
router.register(r'rarities', views.RarityViewSet)
router.register(r'stackables', views.StackableViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'weapons', views.WeaponViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('/', include('')) # login page here
    path('', TemplateView.as_view(template_name='item_management/index.html')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('items/', include('item_management.urls')),
    path('polls/', include('polls.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)