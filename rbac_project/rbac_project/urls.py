# rbac_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rbac.urls')),  # This will include all URL patterns from the rbac app
]
