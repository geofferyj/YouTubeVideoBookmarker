from django.contrib import admin
from bookmarker.models import Token, Subscription, Video, UserVideo, VideoViews, ResetableViews, User

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('vid', 'timestamps', 'locked','cost', 'last_editor',)
    list_filter = ('cost', 'locked')
    list_editable = ["cost", 'locked',]
    search_fields = ['vid',]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid_until', 'date_paid','paypal_subscription_id','has_paid', "has_expired")
    list_filter = ('paid_until', 'date_paid')
    search_fields = ['user',]



@admin.register(UserVideo)
class UserVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video',)

@admin.register(ResetableViews)
class ResetableViewsAdmin(admin.ModelAdmin):
    list_display = ('video', 'count')

@admin.register(VideoViews)
class VideoViewsAdmin(admin.ModelAdmin):
    list_display = ('video', 'user')