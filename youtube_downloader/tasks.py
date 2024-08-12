from celery import shared_task
from yt_dlp import YoutubeDL

@shared_task
def download_video_task(url, resolution):
    ydl_opts = {
        'format': resolution,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True  # Playlist indirme yerine sadece tek bir video indirir
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
