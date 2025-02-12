import yt_dlp
import os

# Read cleaned YouTube links
with open('cleaned_youtube_links.csv', 'r') as file:
    links = [line.strip() for line in file.readlines()]

# Create a directory to save audio files
if not os.path.exists('downloaded_audios'):
    os.makedirs('downloaded_audios')

# Define download options for audio only
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded_audios/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Download audio for each link
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for link in links:
        try:
            print(f"Downloading audio from: {link}")
            ydl.download([link])
        except Exception as e:
            print(f"Failed to download {link}: {e}")

print("Audio download completed!")
