import csv
import requests

API_KEY = '779e244689mshf4ab74677251c6bp1043e6jsn78b7d5df499f'  # Your RapidAPI Key
url = "https://youtube-media-downloader.p.rapidapi.com/search"  # API endpoint

# Correct Headers from API documentation
headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "youtube-media-downloader.p.rapidapi.com",
    'Content-Type': "application/x-www-form-urlencoded"
}

query = input("Enter search keyword: ")

# Adjust parameters as needed
params = {
    "query": query,
    "hl": "en",
    "gl": "US",
    "maxResults": 50
}

all_videos = []
next_page_token = None

while len(all_videos) < 500:  
    if next_page_token:
        params['pageToken'] = next_page_token

    # Making the GET request
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        contents = data.get('items', [])

        for video in contents:
            video_id = video.get('id', {}).get('videoId')
            title = video.get('snippet', {}).get('title')
            views = video.get('statistics', {}).get('viewCount', 'N/A')
            duration = video.get('contentDetails', {}).get('duration', 'N/A')

            if video_id and title:
                all_videos.append([title, f"https://www.youtube.com/watch?v={video_id}", views, duration])

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break
    else:
        print("Error:", response.status_code, response.text)
        break

# Save Data to CSV
with open("youtube_dataset.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Link", "Views", "Duration"])  # Column headers
    writer.writerows(all_videos)

print("✅ Dataset saved as 'youtube_dataset.csv'")
