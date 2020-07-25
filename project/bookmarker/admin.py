from django.contrib import admin
from bookmarker.models import Subscription, Token, Video, PromoCode
admin.site.register(Subscription)
admin.site.register(Token)


class PromoCodeInline(admin.TabularInline):
    model = PromoCode.user.through
class UserAdmin(admin.ModelAdmin):
    inlines = [
        PromoCodeInline,
    ]
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vid', 'timestamps', 'locked','cost', 'hits',)
    list_filter = ("timestamps","user", "hits",)
    list_editable = ["cost", 'locked',]
    search_fields = ['vid', 'user',]

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    inlines = [
        PromoCodeInline,
    ]
    exclude = ('user',)
