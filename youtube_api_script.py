import csv
import requests
import time
import os

API_KEY = '779e244689mshf4ab74677251c6bp1043e6jsn78b7d5df499f'
url = "https://youtube-v31.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "youtube-v31.p.rapidapi.com"
}

query = input("Enter search keyword: ")

params = {
    "q": query,
    "part": "snippet",
    "maxResults": 50,   # Max allowed per API call
    "type": "video"
}

videos = []
next_page_token = None

# Load existing links to avoid duplicates
existing_links = set()
if os.path.exists("youtube_links.csv"):
    with open("youtube_links.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            existing_links.add(row[1])  # Add existing video links to the set

while True:
    if next_page_token:
        params["pageToken"] = next_page_token  # Add nextPageToken if available

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])

        if not items:
            print("No more videos found.")
            break

        for item in items:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            link = f"https://www.youtube.com/watch?v={video_id}"
            
            # Check for duplicates before adding
            if link not in existing_links:
                videos.append([title, link])
                existing_links.add(link)

        # Check if there is another page
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break  # Exit loop if no more pages
        
        time.sleep(1)  # Add delay to avoid rate limiting

    else:
        print("Error:", response.status_code, response.text)
        break

# Append new videos to the existing CSV
if videos:
    with open("youtube_links.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(videos)
    print(f"✅ {len(videos)} new links added to 'youtube_links.csv'")
else:
    print("No new videos found to add.")
