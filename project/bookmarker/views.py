import uuid
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.utils.decorators import method_decorator

from bookmarker.models import  Video, HitCounter

# /watch
# view for the home page


class Index(View):

    def __init__(self):
        self.video = {}

    def return_fun(self):
        return render(self.request, 
        'bookmarker/index.html', 
        {'video': self.video})

    def get(self, request, *args, **kwargs):
        if request.GET.get('v'): 

            video_id = request.GET['v'][-11:]  
            user = request.user 
            
            if user.is_authenticated:
                try:
                    self.video = user.videos.get(vid=video_id)
                    return self.return_fun()
                except Video.DoesNotExist:
                    self.video, _ = Video.objects.get_or_create(vid=video_id)

            else:
                    self.video, _ = Video.objects.get_or_create(vid=video_id)

            
            if self.video.locked:

                if user.is_authenticated:
                    if not user.subscription.expired:
                        return self.return_fun()
                    elif user.tokens.amount >= self.video.cost:
                        user.tokens.amount -= self.video.cost
                        user.videos.add(self.video)
                        user.tokens.save()
                        return self.return_fun()
                    else:
                        messages.error(request, "Sorry You need sufficient tokens or a subscription to watch this video")
                else:
                    messages.error(request, "Sorry You need be logged in to watch this video")
                    return redirect('login')
            else:
                return self.return_fun()
                
        return self.return_fun()

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs): 
        user = request.user
        video_id = request.GET['v'][-11:]
        self.timestamps = request.POST.get('timestamps').strip()  # get and clean timestamps from webpage
        
        # Begin recaptcha verification
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = { 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response 
                }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()   

        # if recaptcha was successful
        if result.get('success'):
            self.video, _ = Video.objects.get_or_create(user=user, vid=video_id)
            if not self.video.timestamps:
                user.tokens.amount += 3
                user.tokens.save()    
                self.video.timestamps = self.timestamps  # 
                self.video.save()        
            else:
                user.tokens.amount += 1
                user.tokens.save()
                self.video.timestamps = self.timestamps  # 
                self.video.save()  

            url = f"{request.path_info}?v={video_id}"  # build a path to redirect to if post operation is complete
            return redirect(url)
        else:  # if recaptcha was unsuccessful
            messages.error(request, 'reCAPTCHA error. Please try again.')  # return an error
        # End recaptcha verification     

        return self.return_fun()
    

class Count(View):
    def post(self, request):
        if request.is_ajax(): 
            user = request.user
            vid = request.POST.get('vid')
            Video = Video.objects.get(user=user, vid=vid)
            
            if user.is_authenticated:
                hit = HitCounter.objects.get_or_create(user=user, video=video)
                hit.hit += 1
                hit.save() 
        return JsonResponse({'error':'supports only POST requests'}, status=400)
# /
# simply redirects all request to this route to the /watch route
def red(request):
    return redirect('index')


# <secret_link>/
# view for the secret page
def get_secret_page(request, link):
    video_id = None
    timestamps = ''
    blocked = ''
    get_object_or_404(SecretLink, link=link, expires__gte=datetime.now())  # check that the link has not expired

    # if the request is a GET request
    if request.method == 'GET' and request.GET.get('v'): 

        video_id = request.GET['v'][-11:]  # extracts the last 11 characters of the youtube video url
                                            # YouTube Video ids are 11 digits long 

        # if video with this video_id exists,   
        try:
            video = Video.objects.get(pk=video_id)  # retrive video object and assign to video
        except Video.DoesNotExist:  # if video with this video_id does not exist,   
            video = Video(vid=video_id, timeStamps=timestamps, blocked=blocked)  # create video object, assign to video
            video.save()  # save object to db
        
        timestamps = video.timeStamps  # timestamps to send back to the webpage
        blocked = video.blocked  # blocked status to send back to the webpage
    
    #  if the request is a POST request
    elif request.method == 'POST': 
        video_id = request.GET['v'][-11:]
        timestamps = request.POST.get('timestamps').strip()  # get and clean timestamps from webpage
        video = Video.objects.get(pk=video_id)
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
            video.timeStamps = timestamps  # 
            video.blocked = blocked  # save video
            video.save()  #
        else:  # if recaptcha was unsuccessful
            messages.error(request, 'reCAPTCHA error. Please try again.')  # return an error
        # End recaptcha verification     
            
        url = f"{request.path_info}?v={video_id}"  # build a path to redirect to if post operation is complete
        return redirect(url)

    return render(request, 'bookmarker/index.html', {'video': video_id, 'timestamps': timestamps, 'hidden_page':True, 'blocked': blocked})


# generate/
# view that generates secret links for the secret page
def generate_secret_link(request):
    
    if request.method == 'POST' and request.is_ajax(): 
        days = float(request.POST.get('days'))
        hours = float(request.POST.get('hours'))
        minutes = float(request.POST.get('minutes'))
        link = uuid.uuid4()  # creates a string of random characters using the uuid library
        expiring_date = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)  # current time + age of link = expiring_date

        try:
            s_link = SecretLink.objects.get(pk=1)  # ensures there is only one link at anygiven time
            s_link.link = link  #
            s_link.expires = expiring_date  # if link object exist update object with new info
            s_link.save()  #

        except SecretLink.DoesNotExist:  # if link object doesn't exist, create new link object with new info
            SecretLink.objects.create(link=link, expires=expiring_date)
            
        response = {'link':link}
        return JsonResponse(response, status=201)  # sends link back in JSON format
    return JsonResponse({'error':'supports only POST requests'}, status=400)


@login_required
# admin/
# view for the admin page
def admin_page(request):
    video_ids = []
    videos = []
    video_url = 'https://www.googleapis.com/youtube/v3/videos'  # the youtube api route
    
    for i in Video.objects.all():  # gets and store all video ids in the db to video_ids
        video_ids.append(i.vid)

    # parameters for the request to youtube api
    video_params = { 
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet',
            'id' : ','.join(video_ids),
        }

    r = requests.get(video_url, params=video_params)  # the request to the api

    results = r.json()['items']  # converts the result into JSON format and selects the items list 
        
    for result in results:  # gets every video in the items list and stored their details in videos list
        video = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }

        videos.append(video)

    return render(request, 'bookmarker/admin_page.html', {'videos': videos, })


def recog(request):
    return render(request, 'bookmarker/testt.html')

# def index(request):
#     video = None
#     timestamps = ''
#     blocked = ''

#     # if the request is a GET request
#     if request.method == 'GET' and request.GET.get('v'): 

#         video_id = request.GET['v'][-11:] # extracts the last 11 characters of the youtube video url
#         user = request.user                                 # YouTube Video ids are 11 digits long 

#         # if video with this video_id exists,   
#         try:
#             video = Video.objects.get(pk=video_id) # retrive video object and assign to video
#         except Video.DoesNotExist: # if video with this video_id does not exist,   
#             video = Video(vid=video_id, timeStamps=timestamps, blocked=blocked) # create video object, assign to video
#             video.save() # save object to db
        
#         if video.cost:
#             if user.is_authenticated:

#                 if user.tokens.amount >= video.cost:
#                     user.tokens.amount = user.tokens.amount - video.cost
#                     user.tokens.save()
#                     video = video_id 
#                     timestamps = video.timeStamps # timestamps to send back to the webpage
#                     blocked = video.blocked # blocked status to send back to the webpage
#                 else:
#                     messages.error(request, "Sorry You don't have sufficient tokens to watch this video")
#             else:
#                 return redirect('login')
#         else:
#             video = video_id
#             timestamps = video.timeStamps # timestamps to send back to the webpage
#             blocked = video.blocked # blocked status to send back to the webpage
    
#     #  if the request is a POST request
#     elif request.method == 'POST': 
#         if request.POST.get('blocked'):
#             blocked = 'checked'
#         else:
#             video_id = request.GET['v'][-11:]
#             timestamps = request.POST.get('timestamps').strip() # get and clean timestamps from webpage
#             video = Video.objects.get(pk=video_id)
#             vt = video.timeStamps
#             user = request.user

#             if not vt:
#                 user.tokens.amount += 3
#                 user.tokens.save()
#             else:
#                 user.tokens.amount += 1
#                 user.tokens.save()

#             # Begin recaptcha verification
#             recaptcha_response = request.POST.get('g-recaptcha-response')
#             data = { 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
#                     'response': recaptcha_response 
#                     }
#             r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
#             result = r.json()   

#             # if recaptcha was successful
#             if result.get('success'):
#                 video.timeStamps = timestamps  # 
#                 video.blocked = blocked        # save video
#                 video.save()                   #
#             else: # if recaptcha was unsuccessful
#                 messages.error(request, 'reCAPTCHA error. Please try again.')  # return an error
#             # End recaptcha verification     
                
#             url = f"{request.path_info}?v={video_id}" # build a path to redirect to if post operation is complete
#             return redirect(url)

#     return render(request, 'bookmarker/index.html',{'video': video, 'timestamps':timestamps, 'hidden_page': False, 'blocked':blocked})
