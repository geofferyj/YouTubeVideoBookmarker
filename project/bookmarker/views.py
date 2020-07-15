import uuid, requests
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from bookmarker.models import VideoData, SecretLink
from django.contrib.auth.decorators import login_required




def index(request):
    video = None
    timestamps = ''
    blocked = ''

    if request.method == 'GET' and request.GET.get('v'):

        video_id = request.GET['v'][-11:]

        try:
            video_data = VideoData.objects.get(pk=video_id)
        except VideoData.DoesNotExist:
            video_data = VideoData(vid=video_id, timeStamps=timestamps, blocked=blocked)
            video_data.save()
        
        video = video_data.vid
        timestamps = video_data.timeStamps
        blocked = video_data.blocked
        
    elif request.method == 'POST':
        blocked = ''

        video_id = request.GET['v'][-11:]
        timestamps = request.POST.get('timestamps').strip()
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if request.POST.get('blocked'):
            blocked = 'checked'
        
        video_data = VideoData.objects.get(pk=video_id)
        
        if result.get('success'):
            video_data.timeStamps = timestamps
            video_data.blocked = blocked
            video_data.save()
            video = video_data.vid
        
            
        url = f"{request.path_info}?v={video_id}"
        return redirect(url)

    return render(request, 'bookmarker/index.html',{'video': video, 'timestamps':timestamps, 'hidden_page': False, 'blocked':blocked})


def red(request):
    return redirect(index)


def get_secret_page(request, link):

    secret_link = get_object_or_404(SecretLink, link=link, expires__gte=datetime.now())

    if request.method == 'GET':
        video_id = secret_link.video.vid
        timestamps = secret_link.video.timeStamps
        blocked = secret_link.video.blocked
        
    elif request.method == 'POST':
        blocked = ''

        video_id = secret_link.video.vid
        video_data = VideoData.objects.get(pk=video_id)

        if request.POST.get('blocked'):
            blocked = 'checked'

        timestamps = request.POST.get('timestamps').strip()
        video_data.timeStamps = timestamps
        video_data.blocked = blocked
        video_data.save()
        video_id = video_data.vid
        return redirect(request.path_info)

    return render(request, 'bookmarker/index.html',{'video': video_id, 'timestamps': timestamps, 'hidden_page':True, 'blocked': blocked})


def generate_secret_link(request):

    if request.method == 'POST' and request.is_ajax():
        days = float(request.POST.get('days'))
        hours = float(request.POST.get('hours'))
        minutes = float(request.POST.get('minutes'))
        link = uuid.uuid4()
        expiring_date = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
        video_id = request.POST.get('video_id')
        video = VideoData.objects.get(vid=video_id)

        try:
            s_link = SecretLink.objects.get(video=video)
            s_link.link = link
            s_link.expires = expiring_date
            s_link.save()

        except SecretLink.DoesNotExist:
            SecretLink.objects.create(link=link,expires=expiring_date, video=video)
            
        response = {'link':link}
        return JsonResponse(response, status=201)
    return JsonResponse({'error':'supports only POST requests'}, status=400)


@login_required
def admin_page(request):
    video_ids = []
    videos = []
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    
    for i in VideoData.objects.all():
        video_ids.append(i.vid)

    video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet',
            'id' : ','.join(video_ids),
        }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']

        
    for result in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }

        videos.append(video_data)

    return render(request, 'bookmarker/admin_page.html',{'videos': videos,})

