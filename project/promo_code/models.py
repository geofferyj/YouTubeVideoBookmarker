from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
PURPOSE = [
    ('Token', 'Token'),
    ('Subscription', 'Subscription')
]
class PromoCode(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    dur = models.PositiveIntegerField(default=0)
    purpose = models.CharField(choices=PURPOSE, max_length=20)
    token_amount = models.PositiveIntegerField(default=0)
    subscription_duration = models.PositiveIntegerField(default=0)
    max_use = models.PositiveIntegerField(default=0)

    @property 
    def duration(self):
        return timedelta(days=float(self.dur))

    @property 
    def is_valid_until(self):
        return self.date_created + self.duration
        
     
    @property
    def has_expired(self):

        expiring_date = self.date_created + self.duration # current time + age of link = expiring_date
        return True if expiring_date <= datetime.now() else False
    
    @property
    def times_used(self):
        return self.users.all().count()

    def __str__(self):
        return self.code


class UserPromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="promo_codes")
    code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name='users')
    date_used = models.DateTimeField(auto_now_add=True)


    @property
    def purpose(self):
        return self.code.purpose
   
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'code'], name='user_promo_codes')
        ]

    def __str__(self):
        return self.user.username