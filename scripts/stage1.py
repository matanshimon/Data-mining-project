import json
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

# Read the video IDs from the file
with open("../data/raw/video_IDS.txt", "r") as f:
    video_ids = f.read().split(',')

# Open the output file
with open("../data/raw/subtitles.txt", "w") as f:
    # Loop over the video IDs
    for video_id in video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Get the video title using pytube
        youtube = YouTube(video_url)
        title = youtube.title

        # Get the transcript using youtube_transcript_api
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

        # Concatenate all the 'text' fields from the transcript segments
        text = ' '.join(i['text'] for i in srt)

        # Create a dictionary with 'title' and 'text' keys
        new_json = {'title': title, 'text': text}

        # Write the dictionary to the file as a JSON object
        f.write(json.dumps(new_json))
        f.write("\n")