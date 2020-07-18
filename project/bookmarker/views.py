import uuid
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from bookmarker.models import SecretLink, VideoData


# /watch
# view for the home page
def index(request):
    video_id = None
    timestamps = ''
    blocked = ''

    # if the request is a GET request
    if request.method == 'GET' and request.GET.get('v'): 

        video_id = request.GET['v'][-11:] # extracts the last 11 characters of the youtube video url
                                          # YouTube Video ids are 11 digits long 

        # if video with this video_id exists,   
        try:
            video_data = VideoData.objects.get(pk=video_id) # retrive video object and assign to video_data
        except VideoData.DoesNotExist: # if video with this video_id does not exist,   
            video_data = VideoData(vid=video_id, timeStamps=timestamps, blocked=blocked) # create video object, assign to video_data
            video_data.save() # save object to db
        
        timestamps = video_data.timeStamps # timestamps to send back to the webpage
        blocked = video_data.blocked # blocked status to send back to the webpage
    
    #  if the request is a POST request
    elif request.method == 'POST': 
        video_id = request.GET['v'][-11:]
        timestamps = request.POST.get('timestamps').strip() # get and clean timestamps from webpage
        video_data = VideoData.objects.get(pk=video_id)
        if request.POST.get('blocked'):
            blocked = 'checked'

        # Begin recaptcha verification
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = { 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                 'response': recaptcha_response 
                }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()   

         # if recaptcha was successful
        if result.get('success'):
            video_data.timeStamps = timestamps  # 
            video_data.blocked = blocked        # save video
            video_data.save()                   #
        else: # if recaptcha was unsuccessful
            messages.error(request, 'reCAPTCHA error. Please try again.')  # return an error
        # End recaptcha verification     
            
        url = f"{request.path_info}?v={video_id}" # build a path to redirect to if post operation is complete
        return redirect(url)

    return render(request, 'bookmarker/index.html',{'video': video_id, 'timestamps':timestamps, 'hidden_page': False, 'blocked':blocked})

# /
# simply redirects all request to this route to the /watch route
def red(request):
    return redirect(index)

# <secret_link>/
# view for the secret page
def get_secret_page(request, link):
    video_id = None
    timestamps = ''
    blocked = ''
    get_object_or_404(SecretLink, link=link, expires__gte=datetime.now()) # check that the link has not expired


    # if the request is a GET request
    if request.method == 'GET' and request.GET.get('v'): 

        video_id = request.GET['v'][-11:] # extracts the last 11 characters of the youtube video url
                                          # YouTube Video ids are 11 digits long 

        # if video with this video_id exists,   
        try:
            video_data = VideoData.objects.get(pk=video_id) # retrive video object and assign to video_data
        except VideoData.DoesNotExist: # if video with this video_id does not exist,   
            video_data = VideoData(vid=video_id, timeStamps=timestamps, blocked=blocked) # create video object, assign to video_data
            video_data.save() # save object to db
        
        timestamps = video_data.timeStamps # timestamps to send back to the webpage
        blocked = video_data.blocked # blocked status to send back to the webpage
    
    #  if the request is a POST request
    elif request.method == 'POST': 
        video_id = request.GET['v'][-11:]
        timestamps = request.POST.get('timestamps').strip() # get and clean timestamps from webpage
        video_data = VideoData.objects.get(pk=video_id)
        if request.POST.get('blocked'):
            blocked = 'checked'

        # Begin recaptcha verification
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = { 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                 'response': recaptcha_response 
                }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()   

         # if recaptcha was successful
        if result.get('success'):
            video_data.timeStamps = timestamps  # 
            video_data.blocked = blocked        # save video
            video_data.save()                   #
        else: # if recaptcha was unsuccessful
            messages.error(request, 'reCAPTCHA error. Please try again.')  # return an error
        # End recaptcha verification     
            
        url = f"{request.path_info}?v={video_id}" # build a path to redirect to if post operation is complete
        return redirect(url)

    return render(request, 'bookmarker/index.html',{'video': video_id, 'timestamps': timestamps, 'hidden_page':True, 'blocked': blocked})

# generate/
# view that generates secret links for the secret page
def generate_secret_link(request):
    
    if request.method == 'POST' and request.is_ajax(): 
        days = float(request.POST.get('days'))
        hours = float(request.POST.get('hours'))
        minutes = float(request.POST.get('minutes'))
        link = uuid.uuid4() # creates a string of random characters using the uuid library
        expiring_date = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes) # current time + age of link = expiring_date

        try:
            s_link = SecretLink.objects.get(pk=1) # ensures there is only one link at anygiven time
            s_link.link = link              #
            s_link.expires = expiring_date  # if link object exist update object with new info
            s_link.save()                   #

        except SecretLink.DoesNotExist: # if link object doesn't exist, create new link object with new info
            SecretLink.objects.create(link=link,expires=expiring_date)
            
        response = {'link':link}
        return JsonResponse(response, status=201) # sends link back in JSON format
    return JsonResponse({'error':'supports only POST requests'}, status=400)


@login_required
# admin/
# view for the admin page
def admin_page(request):
    video_ids = []
    videos = []
    video_url = 'https://www.googleapis.com/youtube/v3/videos' # the youtube api route
    
    for i in VideoData.objects.all(): # gets and store all video ids in the db to video_ids
        video_ids.append(i.vid)

    # parameters for the request to youtube api
    video_params = { 
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet',
            'id' : ','.join(video_ids),
        }

    r = requests.get(video_url, params=video_params) # the request to the api

    results = r.json()['items'] # converts the result into JSON format and selects the items list 

        
    for result in results: # gets every video in the items list and stored their details in videos list
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }

        videos.append(video_data)

    return render(request, 'bookmarker/admin_page.html',{'videos': videos,})

def recog(request):
    return render(request, 'bookmarker/testt.html')