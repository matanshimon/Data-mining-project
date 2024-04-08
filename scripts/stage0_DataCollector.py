import os
from googleapiclient.discovery import build
from tmdbv3api import TMDb, Movie, Genre
import pandas as pd
from tqdm import tqdm

def collect_initial_data():
    # Set up the YouTube Data API
    api_key = 'AIzaSyCq2cw-qAgF4QwomoF_tJkd6rrwn4mo8h8'  # replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Set up the IMDb API
    tmdb = TMDb()
    tmdb.api_key = 'e94fdc1a052381b958527972e0689035'

    # Collect the video IDs, titles, genres, and whether they have closed captions
    data = []
    next_page_token = None

    movie_obj = Movie()
    # Initialize the Genre object
    genre_obj = Genre()

    # Get a list of all genres
    all_genres = genre_obj.movie_list()

    # Convert the list of genres to a dictionary for easy lookup
    genre_dict = {genre['id']: genre['name'] for genre in all_genres}
    
    with tqdm(total=2, desc="Requests") as pbar_outer:
        for _ in range(2):  # make 2 requests
            # Search for movie trailers
            request = youtube.search().list(
                part='snippet',
                maxResults=50,  # max results per request
                q='movie trailer',
                type='video',
                videoCaption='closedCaption',
                pageToken=next_page_token
            )
            response = request.execute()

            with tqdm(total=len(response['items']), desc="Items", leave=False) as pbar_inner:
                for item in response['items']:
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    
                    # process the title to get only the movie name
                    # trailer teaser | - official
                    # split and trip if any of the above is found at lowest index
                    
                    # List of words that indicate the start of the trailer information
                    trailer_indicators = ['trailer', 'teaser', 'official', '|', '-']
                    
                    # Get the index of the first trailer indicator in the title
                    indices = [title.lower().find(word) for word in trailer_indicators if title.lower().find(word) != -1]
                    start_of_trailer_info = min(indices) if indices else len(title)
                    
                    # Get the movie name from the title
                    movie_name = title[:start_of_trailer_info].strip()
                    
                    genres = []

                    # Search for the movie on IMDb and get its genres
                    search = movie_obj.search(movie_name) # {'page': 1, 'results': {}, 'total_pages': 1, 'total_results': 0}
                    if search.get('total_results') > 0:
                        movie = search.get('results')[0]
                        if movie:
                            genres_ids = movie.get('genre_ids')
                            genres = [genre_dict.get(id, 'Unknown') for id in genres_ids]
                    if(len(genres) == 0):
                        continue
                    data.append({
                        'videoId': video_id,
                        'title': title,
                        'movieName': movie_name,
                        'genres': genres
                    })
                    pbar_inner.update()

            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
            pbar_outer.update()

    # Convert the data to a pandas DataFrame and save it to a CSV file
    df = pd.DataFrame(data)
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to the file
    data0_path = os.path.join(script_dir, "..", "data", "raw", "data0.csv")
    df.to_csv(data0_path, index=False)