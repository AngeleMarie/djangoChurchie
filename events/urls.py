from django.urls import path
from . import views


urlpatterns = [
    # Events URLs
    path('', views.event_index, name='events'),  # List all Events
    path('addEvent/', views.add_event, name='addEvent'),  # Add new Event
    path('editEvent/<int:id>/', views.event_edit, name='editEvent'),  # Edit Event
    path('deleteEvent/<int:id>/', views.delete_event, name='deleteEvent'),  # Delete Event
  path('analytics/', views.analytics, name='analytics'),  # Analytics page

]