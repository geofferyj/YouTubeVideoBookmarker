from django.shortcuts import render

def index(request):
    video = None

    if request.GET.get('v_url'):
        video = request.GET['v_url']
        

    return render(request, 'bookmarker/index.html',{
        'video': video,
    })
