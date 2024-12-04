
from django.urls import path
from . import views


urlpatterns = [
    # Christians URLs
    path('', views.index, name='christians'),  # List all Christians
    path('addChristian', views.add_christian, name='addChristian'),  # Add new Christian
    path('editChristian/<int:id>', views.christian_edit, name='editChristian'),  # Edit Christian
    path('deleteChristian/<int:id>', views.delete_christian, name='deleteChristian'),  # Delete Christian
    path('searchChristians', views.search_christians, name='searchChristians'),  # Search Christians
]