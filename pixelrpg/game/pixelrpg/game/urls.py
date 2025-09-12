from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attack/mage/', views.mage_attack, name='mage_attack'),
    path('attack/assassin/', views.assassin_attack, name='assassin_attack'),
    path('house/', views.house_interior, name='house_interior'),
    path('sea/', views.sea_area, name='sea_area'),
    path('beach/', views.beach_area, name='beach_area'),
]