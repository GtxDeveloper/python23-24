from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('women/', views.women, name='women'),
    path('men/', views.men, name='men'),
    path('unisex/', views.unisex, name='unisex'),
    path('item/<int:pk>', views.item, name='item'),
    path('bag/', views.bag, name='bag'),
    path('bag/add/<int:pk>', views.add_to_bag, name='add_to_bag'),
    path('bag/delete/<int:pk>', views.remove_from_bag, name='remove_from_bag'),
    path('statistics/', views.statistics, name='statistics'),
]
