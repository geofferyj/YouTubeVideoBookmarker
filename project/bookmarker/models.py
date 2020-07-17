from django.db import models

# The video model, saves videodata oto the db
class VideoData(models.Model):
    vid = models.CharField(max_length=11, primary_key=True) 
    timeStamps = models.TextField(blank=True, null=True)
    blocked = models.CharField(max_length=10, default='')

# a model to store the links and expiry date
class SecretLink(models.Model):
    link = models.CharField(max_length=200)
    expires = models.DateTimeField()
