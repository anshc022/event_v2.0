from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/<int:event_id>/', views.register, name='register'),
     path('event/<int:pk>/download-registrations/', views.download_registrations_details, name='event_download_registrations_details'),

    
    
]
