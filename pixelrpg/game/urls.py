from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('house/', views.house_view, name='house'),
]