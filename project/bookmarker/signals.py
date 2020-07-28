from django.db.models.signals import post_save
from bookmarker.models import User
from django.dispatch import receiver
from bookmarker.models import Token, Video, ResetableViews

# Token
@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_token(sender, instance, **kwargs):
    instance.tokens.save()


# ResetableViews
@receiver(post_save, sender=Video)
def create_rviews(sender, instance, created, **kwargs):
    if created:
        ResetableViews.objects.create(video=instance)

@receiver(post_save, sender=Video)
def save_rviews(sender, instance, **kwargs):
    instance.rviews.save()