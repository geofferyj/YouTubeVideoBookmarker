from django.db import models
from django.contrib.auth.models import User

class VideoData(models.Model):
    vid = models.CharField(max_length=11, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    timeStamps = models.TextField(blank=True, null=True)
    blocked = models.CharField(max_length=10, default='')