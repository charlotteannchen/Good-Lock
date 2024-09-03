from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lock_dashboard/', views.lock_dashboard, name='lock_dashboard'),
    path('send_message_to_esp32/', views.send_message_to_esp32, name='send_message_to_esp32'),
    path('get_gps_data/', views.get_gps_data, name='get_gps_data'),
    path('set_locked/', views.set_locked, name='set_locked'),
    path('api/gps-data/', views.receive_gps_data, name='receive_gps_data'), ## 0904 add https
]
