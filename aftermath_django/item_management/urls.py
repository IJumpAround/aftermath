from django.urls import path

from item_management.views import generic_item_view, EditWeaponView
from item_management import views

app_name = 'item_management'
urlpatterns = [
    path('', views.aftermath_index, name='items'),
    path('<str:item_type>/<int:pk>/', generic_item_view, name='item'),
    path('weapon/<int:pk>/edit', EditWeaponView.as_view(), name='edit')
]
