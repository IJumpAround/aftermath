from django.urls import include, path
from rest_framework import routers
from . import views

from item_management import views

app_name = 'item_management'
urlpatterns = [
    path('', views.get_all_items, name='items')
]