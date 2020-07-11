from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from bookmarker.models import VideoData
from bookmarker.forms import SignUpForm




def index(request):
    video = None
    timestamps = ''
    blocked = ''
    user = None

    if request.method == 'GET' and request.GET.get('v'):

        v = request.GET['v'][-11:]

        try:
            vdata = VideoData.objects.get(pk=v)
        except VideoData.DoesNotExist:
            vdata = VideoData(vid=v, timeStamps=timestamps, user=user, blocked=blocked)
            vdata.save()
        
        video = vdata.vid
        user = vdata.user
        timestamps = vdata.timeStamps
        blocked = vdata.blocked
        
    elif request.method == 'POST':

        v = request.GET['v'][-11:]
        vdata = VideoData.objects.get(pk=v)

        if request.POST.get('blocked'):

            blocked = 'checked'

        new_time_stamp = request.POST.get('timestamps').strip()
        new_time_stamp = set(new_time_stamp.split(','))
        timestamps = ','.join(new_time_stamp)
        vdata.timeStamps = timestamps
        vdata.blocked = blocked
        vdata.save()
        video = vdata.vid
        user = vdata.user
        timestamps = vdata.timeStamps
        url = f"{request.path_info}?v={v}"
        return redirect(url)

    return render(request, 'bookmarker/index.html',{'video': video, 'timestamps':timestamps, 'user':request.user, 'blocked':blocked})


def red(request):
    return redirect(index)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'bookmarker/register.html', {'form': form})