from django.shortcuts import render
import yaml

# Create your views here.
def simple_upload(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        f = yaml.full_load(myfile)
        print(f['videos'])

        for i in f.get('videos'):
            print(i.get('id'))
        return render(request, 'filetest/su.html')
    return render(request, 'filetest/su.html')