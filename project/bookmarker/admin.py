from django.contrib import admin
from bookmarker.models import VideoData


@admin.register(VideoData)
class VideoDataAdmin(admin.ModelAdmin):
    list_display = ('vid', 'user', 'timeStamps', 'blocked')

# Register your models here.