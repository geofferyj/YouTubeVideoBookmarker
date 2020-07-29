import uuid
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from bookmarker.models import Video, UserVideo, Token, VideoViews, ResetableViews
from bookmarker.utilities import get_video_details

# /watch
# view for the home page


class Index(View):

    def __init__(self):
        self.video = {}
        self.description = ''

    def return_fun(self):
        return render(self.request, 
        'bookmarker/index.html', 
        {'video': self.video, 'description': self.description })

    def get(self, request, *args, **kwargs):
        if request.GET.get('v'): 

            video_id = request.GET['v'][-11:]  
            user = request.user 
            self.description = get_video_details(video_id).get('description')
            self.video, _ = Video.objects.get_or_create(vid=video_id)

            if self.video.locked:

                if user.is_authenticated:
                    
                    try:
                        user_video = user.videos.get(video=self.video)
                    except ObjectDoesNotExist:
                        user_video = None

                    if user_video:
                        return self.return_fun()
                    elif not user.subscription.expired:
                        return self.return_fun()
                    elif user.tokens.amount >= self.video.cost:
                        user.tokens.amount -= self.video.cost
                        user.tokens.save()
                        user.videos.get_or_create(video=self.video)
                        return self.return_fun()
                    else:
                        messages.error(request, "Sorry You need a subscription or sufficient tokens play this video\
                                                you can get tokens by adding timestamps to available videos")
                        return render(self.request, 'bookmarker/index.html', {'video': None, 'description': self.description })
                else:
                    messages.error(request, "Sorry You need be logged in to watch this video")
                    return render(self.request, 'bookmarker/index.html', {'video': None, 'description': self.description })
            else:
                return self.return_fun()
        return self.return_fun()


    @method_decorator(login_required())
    def post(self, request, *args, **kwargs): 
        user = request.user
        video_id = request.GET['v'][-11:]
        timestamps = request.POST.get('timestamps').strip()  # get and clean timestamps from webpage
        
        # Begin recaptcha verification
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = { 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response 
                }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()   

        # if recaptcha was successful
        if result.get('success'):
            self.video = Video.objects.get(vid=video_id)
            self.video.timestamps = timestamps
            self.video.last_editor = user
            self.video.save()
            user.videos.get_or_create(video=self.video)
            changed = False if self.video.timestamps == timestamps else True
            
            if changed:
                self.video.rviews.count = 0
                self.video.rviews.save()

            url = f"{request.path_info}?v={video_id}"  # build a path to redirect to if post operation is complete
            return redirect(url)
        else:  # if recaptcha was unsuccessful
            messages.error(request, 'reCAPTCHA error. Please try again.')  # return an error    
            url = f"{request.path_info}?v={video_id}"  # build a path to redirect to if post operation is complete
            return redirect(url)
            # End recaptcha verification 

        return self.return_fun()
    

class Count(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'error':'supports only POST requests'}, status=400)
    def post(self, request):
        if request.is_ajax(): 
            user = request.user
            video_id = request.POST.get('video_id')
            video = Video.objects.get(vid=video_id)
            timestamps = request.POST.get('timestamps').strip()
            
            if user.is_authenticated:
                if not VideoViews.objects.filter(video=video, user=user).exists():
                    VideoViews.objects.get_or_create(video=video, user=user)
                    views = video.rviews
                    views.count += 1
                    views.save() 

                    
                    changed = False if video.timestamps == timestamps else True

                    if video.timestamps:
                        if (views.count >= 3) and (not changed):
                            video.locked = True
                            video.save()
                            last_editor = video.last_editor
                            last_editor.tokens.amount += 1
                            last_editor.tokens.save()
                        elif changed:
                            video.rviews.count = 0
                            video.rviews.save()
                            
                    return JsonResponse({'message':'success'}, status=200)
        
        return JsonResponse({'error':'request forbidden'}, status=403)


class BuyToken(View):
    def get(self, request, *args, **kwargs):


        return render(self.request, 'bookmarker/buy_tokens.html')
    def post(self, request):
        if request.is_ajax(): 
            user = request.user
            tokens = request.POST.get('tokens', 0)
            user.tokens.amount += int(tokens)   
            user.tokens.save()          
            return JsonResponse({'message':'success'}, status=200)
        
        return JsonResponse({'error':'request forbidden'}, status=403)


class Subscribe(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'bookmarker/subscribe.html')    

    def post(self, request):
        if request.is_ajax(): 
            user = request.user
            expires = datetime.today() + timedelta(days=30)
            user.set_paid_until(expires.date()) 
            user.save()     
            return JsonResponse({'message':'success'}, status=200)
        
        return JsonResponse({'error':'request forbidden'}, status=403)
# /
# simply redirects all request to this route to the /watch route
def red(request):
    return redirect('index')

# generate/
# view that generates secret links for the secret page

@login_required
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

class StoreView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "bookmarker/store.html")

