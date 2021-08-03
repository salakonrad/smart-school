from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', include('school.urls')),
    path('admin/', admin.site.urls),
]
