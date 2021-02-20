from django.urls import path

from item_management import views

app_name = 'item_management'
urlpatterns = [
    path('', views.MainItemsView.as_view({'get': 'get'}), name='items')
]
