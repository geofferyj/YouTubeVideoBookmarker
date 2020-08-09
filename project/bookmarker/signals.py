from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from bookmarker.models import Token, Video, ResetableViews, Subscription, VoicePause

# VoicePause
@receiver(post_save, sender=User)
def create_voicepause(sender, instance, created, **kwargs):
    if created:
        VoicePause.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_voicepause(sender, instance, **kwargs):
    instance.voice_pause.save()

# Token
@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_token(sender, instance, **kwargs):
    instance.tokens.save()

# Subscription
@receiver(post_save, sender=User)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_subscription(sender, instance, **kwargs):
    instance.subscription.save()

# ResetableViews
@receiver(post_save, sender=Video)
def create_rviews(sender, instance, created, **kwargs):
    if created:
        ResetableViews.objects.create(video=instance)

@receiver(post_save, sender=Video)
def save_rviews(sender, instance, **kwargs):
    instance.rviews.save()
