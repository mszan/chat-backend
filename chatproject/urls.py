from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Chat app urls.
    path('', include('chat.urls')),

    # Admin.
    path('admin/', admin.site.urls),

    # Admin documentation.
    path('admin/doc/', include('django.contrib.admindocs.urls')),
]
