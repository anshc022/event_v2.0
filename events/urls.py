from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('register/<int:event_id>/', views.register, name='register'),
    path('event/<int:pk>/download-registrations/', views.download_registrations_details, name='event_download_registrations_details'),
    path('event/<int:event_id>/add-to-calendar/', views.add_to_calendar, name='add_to_calendar'),
    # Add other paths as needed
]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)