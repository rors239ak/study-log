from django.urls import path
from game import views

urlpatterns = [
    path('', views.index, name='index'),
    path('house/', views.house_interior, name='house_interior'),
    path('sea/', views.sea_area, name='sea_area'),
    path('beach/', views.beach_area, name='beach_area'),
]