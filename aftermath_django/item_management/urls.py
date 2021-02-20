from django.urls import path

from item_management import views
from item_management.views import TestView

app_name = 'item_management'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('all', views.MainItemsView.as_view({'get': 'get'}), name='items'),
    # path('', TestView.as_view())
    path('', TestView.as_view())
]
