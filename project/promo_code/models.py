from django.db import models
from bookmarker.models import User
from datetime import date, datetime, timedelta

class PromoBase(models.Model):
    user = models.ManyToManyField(User, related_name='promo_codes')
    code = models.CharField(max_length=10, primary_key=True)
    hits = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(default=timedelta(0))
    

    
    @property
    def has_expired(self):

        expiring_date = self.date_created + self.duration # current time + age of link = expiring_date
        return True if expiring_date >= datetime.now() else False
    
    def __str__(self):
        return self.code


class TokenCode(PromoBase):
    token_amount = models.PositiveIntegerField(default=0)


    

class SubscriptionCode(PromoBase):
    subscription_duration = models.DurationField(default=timedelta(30))

 