from django.urls import path
from . import views


urlpatterns = [
    path('tickets/', views.ticket_create,), # for ngo and restaurant ticket section
    path('tickets/<int:ticket_id>/update/', views.ticket_update_status), #NGO resvered
]
