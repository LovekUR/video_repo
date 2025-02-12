import csv
import os
import subprocess

# Create folders to store downloaded videos and converted audio
os.makedirs('downloaded_videos', exist_ok=True)
os.makedirs('converted_audios', exist_ok=True)

# Read URLs from CSV
with open('youtube_links.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row if present
    video_data = list(reader)

# Function to download and convert videos
def process_video(title, url):
    sanitized_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in title)
    video_path = f'downloaded_videos/{sanitized_title}.mp4'
    audio_path = f'converted_audios/{sanitized_title}.flac'

    try:
        # Download the video
        print(f"Downloading: {title}")
        subprocess.run(['yt-dlp', '--no-check-certificate', '-o', video_path, url], check=True)

        # Convert to FLAC
        print(f"Converting: {title}")
        subprocess.run(['ffmpeg', '-i', video_path, '-ac', '1', '-vn', '-c:a', 'flac', audio_path], check=True)

        print(f"Successfully processed: {title}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing {title}: {e}")

# Process all videos
for title, url in video_data:
    process_video(title, url)
