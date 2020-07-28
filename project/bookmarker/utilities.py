
import requests
from django.conf import settings

def get_video_details(video_id):
    video_url = 'https://www.googleapis.com/youtube/v3/videos'  # the youtube api route
    video_params = { 
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet',
            'id' : video_id,
        }

    r = requests.get(video_url, params=video_params)  # the request to the api

    result = r.json()['items'][0]['snippet']  # converts the result into JSON format and selects the items list 
    return result
