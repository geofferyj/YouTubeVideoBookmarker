import uuid, requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from bookmarker.models import VideoData, SecretLink



def index(request):
    video = None
    timestamps = ''
    blocked = ''

    if request.method == 'GET' and request.GET.get('v'):

        v = request.GET['v'][-11:]

        try:
            vdata = VideoData.objects.get(pk=v)
        except VideoData.DoesNotExist:
            vdata = VideoData(vid=v, timeStamps=timestamps, blocked=blocked)
            vdata.save()
        
        video = vdata.vid
        timestamps = vdata.timeStamps
        blocked = vdata.blocked
        
    elif request.method == 'POST':

        v = request.GET['v'][-11:]
        timestamps = request.POST.get('timestamps').strip()
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if request.POST.get('blocked'):
            blocked = 'checked'
        
        vdata = VideoData.objects.get(pk=v)
        
        if result['success']:
            vdata.timeStamps = timestamps
            vdata.blocked = blocked
            vdata.save()
            video = vdata.vid
            messages.success(request, 'success!')
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        url = f"{request.path_info}?v={v}"
        return redirect(url)

    return render(request, 'bookmarker/index.html',{'video': video, 'timestamps':timestamps, 'hidden_page': False, 'blocked':blocked})


def red(request):
    return redirect(index)


def secret(request, link):

    s_link = SecretLink.objects.get(link=link)

    if request.method == 'GET':
        v = s_link.video.vid
        timestamps = s_link.video.timeStamps
        blocked = s_link.video.blocked

        # try:
        #     vdata = VideoData.objects.get(pk=v)
        # except VideoData.DoesNotExist:
        #     vdata = VideoData(vid=v, timeStamps=timestamps, blocked=blocked)
        #     vdata.save()
        
    elif request.method == 'POST':

        v = s_link.video.vid
        vdata = VideoData.objects.get(pk=v)

        if request.POST.get('blocked'):
            blocked = 'checked'

        timestamps = request.POST.get('timestamps').strip()
        vdata.timeStamps = timestamps
        vdata.blocked = blocked
        vdata.save()
        video = vdata.vid
        # url = f"{request.path_info}?v={v}"
        print('\n\n\n\n\n\n', request.path_info, '\n\n\n\n\n\n')
        return redirect(request.path_info)

    return render(request, 'bookmarker/index.html',{'video': v, 'timestamps': timestamps, 'hidden_page':True, 'blocked': blocked})


# def admin(request):
