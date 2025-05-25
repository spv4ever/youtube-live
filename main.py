import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Ruta a la carpeta donde están los videos
VIDEO_FOLDER = "videos_reflexion/"
# Extensiones válidas de video
VALID_EXTENSIONS = (".mp4", ".mov", ".mkv", ".avi")
# URL RTMP de YouTube
RTMP_URL = os.getenv("YOUTUBE_RTMP_URL")

def get_video_files():
    files = [os.path.join(VIDEO_FOLDER, f) for f in os.listdir(VIDEO_FOLDER)
             if f.lower().endswith(VALID_EXTENSIONS)]
    return sorted(files)  # orden alfabético

def stream_video(video_path):
    print(f"🔴 Emitiendo: {video_path}")
    process = subprocess.Popen([
        "ffmpeg",
        "-re",
        "-i", video_path,
        "-vf", "scale=w=2560:h=1440:force_original_aspect_ratio=decrease,pad=2560:1440:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "faster",
        "-maxrate", "13500k",
        "-bufsize", "27000k",
        "-pix_fmt", "yuv420p",
        "-g", "50",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-f", "flv",
        RTMP_URL
    ])
    process.wait()

def stream_loop():
    while True:
        video_files = get_video_files()
        if not video_files:
            print("⚠️ No se encontraron videos en la carpeta. Esperando 30s...")
            time.sleep(30)
            continue
        for video in video_files:
            stream_video(video)

if __name__ == "__main__":
    stream_loop()
