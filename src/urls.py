from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # API app urls.
    path('api/', include('api.urls')),

    # Admin.
    path('admin/', admin.site.urls),

    # Admin documentation.
    path('admin/doc/', include('django.contrib.admindocs.urls')),
]
