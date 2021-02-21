from django.urls import path


from item_management import views
from item_management.views import generic_item_view

app_name = 'item_management'
urlpatterns = [
    path('', views.aftermath_index, name='items'),
    path('<str:item_type>/<int:pk>/', generic_item_view, name='weapons'),
]
