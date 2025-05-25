import os
import subprocess

# Ruta a la carpeta original y de salida
INPUT_FOLDER = "videos_reflexion/"
OUTPUT_FOLDER = "converted_reflexion/"

# Crear carpeta de salida si no existe
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Extensiones válidas
VALID_EXTENSIONS = (".mp4", ".mov", ".mkv", ".avi")

def convert_video(input_path, output_path):
    print(f"⚡️ Convertiendo con GPU: {os.path.basename(input_path)}")
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "scale=w=2560:h=1440:force_original_aspect_ratio=decrease,pad=2560:1440:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "h264_nvenc",
        "-b:v", "13500k",
        "-maxrate", "13500k",
        "-bufsize", "27000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-movflags", "+faststart",
        "-y",  # sobrescribe si ya existe
        output_path
    ]
    subprocess.run(command)

def process_all_videos():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(VALID_EXTENSIONS):
            input_path = os.path.join(INPUT_FOLDER, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_1440p.mp4"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            convert_video(input_path, output_path)

if __name__ == "__main__":
    process_all_videos()
