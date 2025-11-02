from django.urls import path
from .import  views


urlpatterns = [
    path('ngo_signup/', views.ngo_register,),
    path('restaurant_signup/',views.rest_register),
    path('login/',views.login_view)
    
    ]