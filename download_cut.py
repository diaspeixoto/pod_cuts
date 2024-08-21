import csv
import re
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import yt_dlp

def sanitize_filename(filename):
    # Substitui espaços por underscores e remove caracteres especiais
    filename = re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')
    return filename

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloaded_video.%(ext)s',  # Save as .mp4
        'merge_output_format': 'mp4',  # Ensure the output is in mp4 format
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'downloaded_video.mp4'

def cut_video(video_path, cuts_csv):
    # Create the 'cuts' folder if it doesn't exist
    if not os.path.exists('cuts'):
        os.makedirs('cuts')

    with open(cuts_csv, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            start_time = convert_to_seconds(row[0])
            end_time = convert_to_seconds(row[1])
            output_filename = os.path.join('cuts', sanitize_filename(row[2]) + '.mp4')  # Save in 'cuts' folder
            ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_filename)

def convert_to_seconds(time_str):
    parts = list(map(int, time_str.split(":")))
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    elif len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=f7xRgss2IOQ&t=1105s"
    cuts_csv = "cortes_flow392_clovis.csv"

    video_path = download_video(video_url)
    #video_path = "downloaded_video.mp4"
    cut_video(video_path, cuts_csv)

    print("Processo concluído!")
