from apps.restaurant import views
from django.urls import path


urlpatterns = [
   path('restaurants/',views.restaurant_list_create, name = 'new_restaurant_create'),
   path('restaurants/<restaurant_id>/update/',views.restaurant_list_create, name = 'new_restaurant_create'),
   path('restaurants/tickets/<int:ticket_id>/delivered/',views.ticket_mark_delivered, name = 'ticket-mark-status'),
]