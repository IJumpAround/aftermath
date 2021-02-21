from django.urls import path


from item_management import views
from item_management.views import WeaponDetailView

app_name = 'item_management'
urlpatterns = [
    path('', views.aftermath_index, name='items'),
    path('weapon/<int:pk>/', WeaponDetailView.as_view(), name='weapons'),
]
