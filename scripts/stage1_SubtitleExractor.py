import os
import json
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from tqdm import tqdm
from stage0_DataCollector import collect_initial_data

# Collect the initial data
#collect_initial_data()
def subtitle_extracttor():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the file
    data0_path = os.path.join(script_dir, "..", "data", "raw", "data0.csv")
    data1_path = os.path.join(script_dir, "..", "data", "raw", "subtitle.json")

    # Read the CSV file
    df = pd.read_csv(data0_path)
    data = df[['videoId', 'genres', 'movieName']].values

    # Open the output file
    with open(data1_path, "w") as f:
        # Loop over the video IDs and genres
        for video_id, genre, name in tqdm(data, desc="Processing videos"):
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Get the video title using pytube
            youtube = YouTube(video_url)

            # Get the list of transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Search for en(any country)
            lang = 'en'
            srt = None 
            for transcript in transcript_list:
                if transcript.language_code.startswith(lang):
                    srt = transcript.fetch()
                    break
            text = ''
            # Concatenate all the 'text' fields from the transcript segments
            if srt:
                text = ' '.join(i['text'] for i in srt)

            # Create a dictionary with 'title', 'text', and 'genre' keys
            new_json = {'movieName': name, 'text': text, 'genre': genre}

            # Write the dictionary to the file as a JSON object
            f.write(json.dumps(new_json))
            f.write("\n")