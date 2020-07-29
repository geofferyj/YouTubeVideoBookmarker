import uuid
from django.shortcuts import render
from django.views.generic import View
from promo_code.forms import TokenCodeForm, SubscriptionCodeForm
from promo_code.models import TokenCode, SubscriptionCode
from datetime import timedelta

class CodeGen(View):
    def get(self, request, *args, **kwargs):
        t_codes = TokenCode.objects.all()
        s_codes = SubscriptionCode.objects.all()
        
        context = {
            "token_codes": t_codes,
            "subscription_codes": s_codes,
        }
        return render(request, "promo_code/code_gen.html", context)
    
    def post(self, request, *args, **kwargs):
    
        code_type = request.POST.get('code_type')
        code = request.POST.get('code')  # creates a string of random characters using the uuid library
        days = int(request.POST.get('days'))
        hours = int(request.POST.get('hours'))
        minutes = int(request.POST.get('minutes'))
        s_days = int(request.POST.get('s_days')) if isinstance(request.POST.get('s_days'), int) else 0
        s_hours = int(request.POST.get('s_hours')) if isinstance(request.POST.get('s_hours'), int) else 0
        s_minutes = int(request.POST.get('s_minutes')) if isinstance(request.POST.get('s_minutes'), int) else 0
        duration = timedelta(days=days, hours=hours, minutes=minutes)
        hits = request.POST.get('hits')

        if code_type == "Token":

            token_amount = request.POST.get("token_amount")
            
            if hits and duration:
                TokenCode.objects.create(code=code, token_amount=token_amount, hits=hits, duration=duration)
            elif hits and not duration:
                TokenCode.objects.create(code=code, token_amount=token_amount, hits=hits)
            
            elif not hits and duration:
                TokenCode.objects.create(code=code, token_amount=token_amount, duration=duration)

            else:
                TokenCode.objects.create(code=code, token_amount=token_amount)

        else:
            sub_dur = timedelta(days=s_days, hours=s_hours, minutes=s_minutes)

            if hits and duration:
                SubscriptionCode.objects.create(code=code, subscription_duration=sub_dur, hits=hits, duration=duration)
            elif hits and not duration:
                SubscriptionCode.objects.create(code=code, subscription_duration=sub_dur, hits=hits)
            
            elif not hits and duration:
                SubscriptionCode.objects.create(code=code, subscription_duration=sub_dur, duration=duration)

            else:
                SubscriptionCode.objects.create(code=code, subscription_duration=sub_dur)

           
            
        return render(request, "promo_code/code_gen.html")




