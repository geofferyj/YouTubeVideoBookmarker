from django.contrib import admin
from promo_code.models import TokenCode, SubscriptionCode



class TokenCodeInline(admin.TabularInline):
    model = TokenCode.user.through

@admin.register(TokenCode)
class TokenCodeAdmin(admin.ModelAdmin):
    inlines = [
        TokenCodeInline,
    ]
    exclude = ('user',)


class SubscriptionCodeInline(admin.TabularInline):
    model = SubscriptionCode.user.through

@admin.register(SubscriptionCode)
class SubscriptionCodeAdmin(admin.ModelAdmin):
    inlines = [
        SubscriptionCodeInline,
    ]
    exclude = ('user',) 