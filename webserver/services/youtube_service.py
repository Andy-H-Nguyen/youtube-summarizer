import yt_dlp
import tempfile

def download_youtube_video(youtube_url: str) -> dict:
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': tempfile.gettempdir() + '/%(title)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        file_path = ydl.prepare_filename(info)
        return {
            "name": info.get('title', 'Unknown Title'),  # Extract the video name (title)
            "thumbnail": info.get('thumbnail'),
            "path": file_path
        }
