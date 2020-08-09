from django.contrib import admin
from bookmarker.models import Token, Subscription, Video, UserVideo, VideoViews, ResetableViews, User, VoicePause

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display: tuple = ('user', 'amount')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display: tuple = ('vid', 'timestamps', 'locked','cost', 'last_editor',)
    list_filter: tuple = ('cost', 'locked')
    list_editable: list = ["cost", 'locked',]
    search_fields:list = ['vid',]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display: tuple = ('user', 'paid_until', 'date_paid','paypal_subscription_id','has_paid', "has_expired")
    list_filter: tuple = ('paid_until', 'date_paid')
    search_fields: list = ['user',]



@admin.register(UserVideo)
class UserVideoAdmin(admin.ModelAdmin):
    list_display: list = ['user', 'video',]

@admin.register(ResetableViews)
class ResetableViewsAdmin(admin.ModelAdmin):
    list_display: list = ['video', 'count']

@admin.register(VideoViews)
class VideoViewsAdmin(admin.ModelAdmin):
    list_display: list = ['video', 'user']
    
    
@admin.register(VoicePause)
class VoicePauseAdmin(admin.ModelAdmin):
    list_display: list = ['user','has']