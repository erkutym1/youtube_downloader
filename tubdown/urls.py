from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('youtube_downloader.urls')),  # Uygulamanızın URLs'ini dahil edin
]
