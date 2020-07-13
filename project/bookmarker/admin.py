from django.contrib import admin
from bookmarker.models import VideoData, SecretLink


@admin.register(VideoData)
class VideoDataAdmin(admin.ModelAdmin):
    list_display = ('vid', 'timeStamps', 'blocked')

# Register your models here.
admin.site.register(SecretLink)