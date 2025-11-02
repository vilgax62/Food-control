
from django.urls import path
from . import views

urlpatterns = [
    path('ngo/',views.ngo_list, name = 'ngo_list'),
    path('ngo/<int:ngo_id>/update/',views.ngo_list, name = 'ngo_list'),
]