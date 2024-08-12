from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # index view eklenmiş
    path('get_resolutions/', views.get_resolutions, name='get_resolutions'),
    path('download_video/', views.download_video, name='download_video'),
    path('get_audio_info/', views.get_audio_info, name='get_audio_info'),
    path('download_audio/', views.download_audio, name='download_audio'),
    path('mp3down/', views.mp3down, name='mp3down'),  # MP3 indirme sayfası için eklenen URL
    path('playlistdownload/', views.playlistdownload, name='playlist'),
    path('get_playlist_info/', views.get_playlist_info, name='get_playlist_info'),
    path('download_playlist/', views.download_playlist, name='download_playlist'),

]
