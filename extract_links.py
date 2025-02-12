import re

# Open the existing CSV file with titles and links
with open('youtube_links.csv', 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# Extract only the YouTube URLs
youtube_links = []
for line in lines:
    match = re.search(r'(https?://www\.youtube\.com/watch\?v=[\w-]+)', line)
    if match:
        youtube_links.append(match.group(1))

# Save the extracted links to a new CSV file
with open('cleaned_youtube_links.csv', 'w', encoding='utf-8') as outfile:
    for link in youtube_links:
        outfile.write(link + '\n')

print(f"Extracted {len(youtube_links)} valid YouTube links!")
