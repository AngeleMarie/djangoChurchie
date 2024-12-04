from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('christians/', include('christians.urls')),
    path('authentication/', include('authentication.urls')),
      path('events/', include('events.urls')),
    path('admin/', admin.site.urls),
]