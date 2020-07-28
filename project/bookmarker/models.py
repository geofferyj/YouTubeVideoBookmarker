from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, timedelta

CODE_PURPOSE = [
    ('T','token'),
    ('S', 'subscription')
]  

class User(AbstractUser):
    paid_until = models.DateField(null=True, blank=True)

    # store one time payment reference to this user
    paypal_order_id = models.CharField(max_length=64, blank=True, null=True)

    # store subscription reference to this user
    paypal_subscription_id = models.CharField(max_length=64, blank=True, null=True)

    def set_paid_until(self, date_or_timestamp):
        if isinstance(date_or_timestamp, int):
            # input date as timestamp integer
            paid_until = date.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, str):
            # input date as timestamp string
            paid_until = date.fromtimestamp(int(date_or_timestamp))
        else:
            paid_until = date_or_timestamp

        self.paid_until = paid_until
        self.save()

    def has_paid(self, current_date=date.today()):
        if self.paid_until is None:
            return False

        return current_date < self.paid_until

# The video model, saves videodata to the db
class Video(models.Model):
    vid = models.CharField(max_length=11, primary_key=True) 
    timestamps = models.TextField(default='')
    cost = models.PositiveIntegerField(default=0)
    locked = models.BooleanField(default=False)
    last_editor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.vid
    
class UserVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="users")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'video'], name='user_video_constraint')
        ]

class Token(models.Model):
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

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
        expiring_date = self.date_created + timedelta(days=self.duration)  # current time + age of link = expiring_date
        return True if expiring_date >= datetime.now() else False
    
    def __str__(self):
        return self.code
    
class ResetableViews(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name='rviews')
    count = models.PositiveIntegerField(default=0)

class VideoViews(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="views")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'video'], name='video_views_constraint')
        ]

