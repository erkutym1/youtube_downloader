from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_video_info, download_video_function, download_audio_function, get_playlist_info_utils, download_playlist_function

import sys
sys.stdout.reconfigure(encoding='utf-8')


def index(request):
    return render(request, 'youtube_downloader/index.html')

def get_resolutions(request):
    video_url = request.GET.get('video_url')
    if not video_url:
        return JsonResponse({'error': 'No video URL provided.'}, status=400)

    try:
        video_info = get_video_info(video_url)
        return JsonResponse(video_info)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def download_video(request):
    video_url = request.GET.get('video_url')
    resolution = request.GET.get('resolution')
    if not video_url or not resolution:
        return JsonResponse({'error': 'Video URL and resolution are required.'}, status=400)

    try:
        download_video_function(video_url, resolution)
        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error during download: {e}")  # Hata mesajını logla
        return JsonResponse({'error': str(e)}, status=500)

def get_audio_info(request):
    video_url = request.GET.get('video_url')
    if not video_url:
        return JsonResponse({'error': 'No video URL provided.'}, status=400)

    try:
        video_info = get_video_info(video_url)
        return JsonResponse(video_info)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def download_audio(request):
    video_url = request.GET.get('video_url')
    bitrate = request.GET.get('bitrate')
    if not video_url or not bitrate:
        return JsonResponse({'error': 'Video URL and bitrate are required.'}, status=400)

    try:
        download_audio_function(video_url, bitrate)
        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error during download: {e}")  # Hata mesajını logla
        return JsonResponse({'error': str(e)}, status=500)

def mp3down(request):
    return render(request, 'youtube_downloader/mp3down.html')

def playlistdownload(request):
    return render(request, 'youtube_downloader/playlist.html')

def get_playlist_info(request):
    playlist_url = request.GET.get('playlist_url')
    if not playlist_url:
        return JsonResponse({'error': 'No playlist URL provided.'}, status=400)

    try:
        playlist_info = get_playlist_info_utils(playlist_url)
        return JsonResponse(playlist_info)
    except Exception as e:
        print(f"Error during playlist info retrieval: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def download_playlist(request):
    playlist_url = request.GET.get('playlist_url')
    download_type = request.GET.get('type')
    resolution = request.GET.get('resolution')

    if not playlist_url or not download_type:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    try:
        output_dir = download_playlist_function(playlist_url, download_type, resolution)
        return JsonResponse({'success': True, 'directory': output_dir})
    except Exception as e:
        print(f"Error during playlist download: {e}")
        return JsonResponse({'error': str(e)}, status=500)
