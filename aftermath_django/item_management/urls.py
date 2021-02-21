from django.urls import path


from item_management import views
from item_management.views import TestView, WeaponDetailView

app_name = 'item_management'
urlpatterns = [
    # path('', views.TemplateView.as_view(template_name='item_management/index.html'), name='index'),
    path('', views.aftermath_index, name='items'),
    path('weapons/<int:pk>/', WeaponDetailView.as_view(), name='weapons'),
    path('a', TestView.as_view())
]
