from django.contrib import admin
from bookmarker.models import Token, Video, PromoCode, UserVideo, VideoViews, ResetableViews, User
admin.site.register(Token)


class PromoCodeInline(admin.TabularInline):
    model = PromoCode.user.through

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'paid_until', 'has_paid',)
    inlines = [
        PromoCodeInline,
    ]
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('vid', 'timestamps', 'locked','cost', 'last_editor',)
    list_filter = ('cost', 'locked')
    list_editable = ["cost", 'locked',]
    search_fields = ['vid',]

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    inlines = [
        PromoCodeInline,
    ]
    exclude = ('user',)

@admin.register(UserVideo)
class UserVideoAdmin(admin.ModelAdmin):
    list_display = ('user', 'video',)

@admin.register(ResetableViews)
class ResetableViewsAdmin(admin.ModelAdmin):
    list_display = ('video', 'count')

@admin.register(VideoViews)
class VideoViewsAdmin(admin.ModelAdmin):
    list_display = ('video', 'user')