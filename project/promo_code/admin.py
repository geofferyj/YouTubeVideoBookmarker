from django.contrib import admin
from promo_code.models import PromoCode, UserPromoCode



@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code','date_created', 'purpose', 'duration', 'is_valid_until', 'has_expired', 'times_used', 'token_amount', 'subscription_duration')

@admin.register(UserPromoCode)
class UserPromoCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code','date_used', 'purpose')
