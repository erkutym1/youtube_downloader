import yt_dlp
import os
import re
import unicodedata
from yt_dlp import YoutubeDL

import sys
sys.stdout.reconfigure(encoding='utf-8')


# Dosya adındaki özel karakterleri temizler
def sanitize_filename(filename):
    # Normalize edilmiş karakterleri normalize eder
    filename = unicodedata.normalize('NFKD', filename)

    # Türkçe ve diğer özel karakterleri ASCII karakterlerle değiştirir
    replacements = {
        'ü': 'u', 'Ü': 'U',
        'ı': 'i', 'I': 'I',
        'ş': 's', 'Ş': 'S',
        'ç': 'c', 'Ç': 'C',
        'ğ': 'g', 'Ğ': 'G',
        'ö': 'o', 'Ö': 'O',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'Â': 'A', 'Ê': 'E', 'Î': 'I', 'Ô': 'O', 'Û': 'U',
        '|': '-',  # FULLWIDTH VERTICAL LINE (U+FF5C) karakterini temizler
    }

    # Replacements kullanarak karakterleri değiştirir
    for char, replacement in replacements.items():
        filename = filename.replace(char, replacement)

    # Geçersiz karakterleri temizler
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    # UTF-8 ile encode eder ve decode eder
    filename = filename.encode('utf-8', 'ignore').decode('utf-8')

    return filename


# İndirme ilerlemesini bildirir
def download_progress(d):
    if d['status'] == 'downloading':
        percent = d.get('percent', 0)
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)
        print(f"[download] {percent}% of {d['filename']} at {speed} ETA {eta}")


# Video bilgilerini alır
def get_video_info(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'No title available')
            formats = info.get('formats', [])
            resolutions = sorted(set(f['height'] for f in formats if f.get('height')), reverse=True)
            return {'title': title, 'resolutions': resolutions}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


# Dosya yolunu siler
def delete_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {str(e)}")


# Video indirme fonksiyonu
def download_video_function(video_url, resolution):
    DOWNLOAD_DIR = os.path.expanduser('~/Downloads/tubdown')
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Klasörü oluşturur, eğer yoksa

    ydl_opts = {
        'format': f'bestvideo[height={resolution}]+bestaudio/best',
        'noplaylist': True,
        'outtmpl': os.path.join(DOWNLOAD_DIR, sanitize_filename('%(title)s.%(ext)s')),  # Dosya yolu
        'progress_hooks': [download_progress],  # İlerleme bildirimleri için
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return DOWNLOAD_DIR
    except Exception as e:
        print(f"Failed to download video: {str(e)}")
        raise


# Ses indirme fonksiyonu
def download_audio_function(video_url, quality):
    DOWNLOAD_DIR = os.path.expanduser('~/Downloads/tubdown')
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Klasörü oluşturur, eğer yoksa

    ydl_opts = {
        'format': f'bestaudio[abr<={quality}]',
        'noplaylist': True,  # Sadece tek bir video indir
        'outtmpl': os.path.join(DOWNLOAD_DIR, sanitize_filename('%(title)s.%(ext)s')),  # Dosya adını temizler
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }],
        'progress_hooks': [download_progress],  # İlerleme bildirimleri için
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return True
    except Exception as e:
        print(f"Error during download: {e}")
        return False


# Playlist bilgilerini alır
def get_playlist_info_utils(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            title = info.get('title', 'No title available')
            return {'title': title, 'videos': info.get('entries', [])}
    except Exception as e:
        print(f"Error retrieving playlist info: {e}")
        raise


# Playlist indirme fonksiyonu
def download_playlist_function(playlist_url, download_type, resolution=None):
    DOWNLOAD_DIR = os.path.expanduser('~/Downloads/tubdown')
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, sanitize_filename('%(playlist_title)s/%(title)s.%(ext)s')),
        'quiet': True,
        'progress_hooks': [download_progress],
    }

    if download_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts[
            'format'] = f'bestvideo[height<={resolution}]+bestaudio/best' if resolution else 'bestvideo+bestaudio/best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            ydl.download([playlist_url])
            playlist_title = sanitize_filename(playlist_info.get('title', 'unknown'))
            return os.path.join(DOWNLOAD_DIR, playlist_title)
    except Exception as e:
        print(f"An error occurred during playlist download: {e}")
        raise
