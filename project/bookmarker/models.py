from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz


CODE_PURPOSE = [
    ('T','token'),
    ('S', 'subscription')
]  


# The video model, saves videodata oto the db
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', default=1)
    vid = models.CharField(max_length=11) 
    timestamps = models.TextField(default='')
    cost = models.PositiveIntegerField(default=0)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.vid
    


# a model for the subscriptions
class Subscription(models.Model):
    user = models.OneToOneField(User, related_name='subscription', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=30)
    
    @property
    def expired(self):
        expiring_date = self.date_created + tz.timedelta(days=self.duration)  # current time + age of link = expiring_date
        return True if expiring_date >= tz.now() else False

    # def __str__(self):
    #     return self.user
    

class Token(models.Model):
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.user

class PromoCode(models.Model):
    user = models.ManyToManyField(User, related_name='promo_codes')
    code = models.CharField(max_length=100, primary_key=True)
    purpose = models.CharField(max_length=10, choices=CODE_PURPOSE)
    token_amount = models.PositiveIntegerField(default=0)
    subscription_duration = models.PositiveIntegerField(default=0)
    hits = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=30)


    @property
    def expired(self):
        expiring_date = self.date_created + tz.timedelta(days=self.duration)  # current time + age of link = expiring_date
        return True if expiring_date >= tz.now() else False
    
    def __str__(self):
        return self.code
    
class HitCounter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='hits')
    count = models.PositiveIntegerField(default=0)