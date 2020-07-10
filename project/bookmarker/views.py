from django.shortcuts import render, redirect
from bookmarker.models import VideoData
from django.contrib.auth.models import User


def index(request):
    video = None
    user = None
    timestamps = 0
    if request.method == 'GET' and request.GET.get('v'):
        v = request.GET['v'][-11:]
        try:
            vdata = VideoData.objects.get(pk=v)
        except VideoData.DoesNotExist:
            if request.user.is_anonymous:
                vdata = VideoData(vid=v, timeStamps=timestamps)
            else:
                vdata = VideoData(vid=v, timeStamps=timestamps, user=request.user)

            vdata.save()
        
        video = vdata.vid
        user = vdata.user
        timestamps = vdata.timeStamps

    elif request.method == 'POST':
        v = request.GET.get('v')
        vdata = VideoData.objects.get(pk=v)
        new_time_stamp = request.POST.get('timestamps').strip()
        new_time_stamp = set(new_time_stamp.split(','))
        timestamps = ','.join(new_time_stamp)
        vdata.timeStamps = timestamps
        vdata.save()
        video = vdata.vid
        user = vdata.user
        timestamps = vdata.timeStamps
        url = f"{request.path_info}?v={v}"
        return redirect(url)

    return render(request, 'bookmarker/index.html',{'video': video, 'timestamps':timestamps, 'user':user})


def red(request):
    return redirect(index)
