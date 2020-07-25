from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from bookmarker.models import Subscription, Token


@receiver(post_save, sender=User)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_subscription(sender, instance, **kwargs):
    instance.subscription.save()

@receiver(post_save, sender=User)
def save_token(sender, instance, **kwargs):
    instance.tokens.save()
