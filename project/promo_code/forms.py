from django.forms import ModelForm
from promo_code.models import TokenCode, SubscriptionCode

class TokenCodeForm(ModelForm):
    class Meta:
        model = TokenCode
        fields = ('code', 'token_amount', 'duration', 'hits')

class SubscriptionCodeForm(ModelForm):
    class Meta:
        model = SubscriptionCode
        fields = ('code', 'subscription_duration', 'duration', 'hits')
 