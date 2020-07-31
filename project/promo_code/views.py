import uuid
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, DeleteView
from promo_code.models import PromoCode
from datetime import timedelta, datetime
from django.db import IntegrityError
from django.contrib import messages
from promo_code.models import UserPromoCode
from django.core.exceptions import ObjectDoesNotExist




class CodeGen(View):
    def get(self, request, *args, **kwargs):
        codes = PromoCode.objects.all().order_by('-date_created')      
        context = {
            "codes": codes,
        }
        return render(request, "promo_code/code_gen.html", context)
    
    def post(self, request, *args, **kwargs):
    
        purpose = request.POST.get('purpose')
        print(purpose)
        code = request.POST.get('code')  # creates a string of random characters using the uuid library
        max_use = float(request.POST.get('max_use')) or 0
        duration = float(request.POST.get('days'))
        sub_dur = float(request.POST.get('s_days')) or 0
        token_amount = float(request.POST.get("token_amount")) or 0
        try:
            PromoCode.objects.create(code=code, token_amount=token_amount, dur=duration, purpose=purpose, subscription_duration=sub_dur, max_use=max_use)
        except IntegrityError as e:
            messages.error(request, 'Code Already exists')
            return redirect('code_gen')

                
        return redirect('code_gen')

 
class UseCode(View):
    def post(self, request, *args, **kwargs):
        p_code = request.POST.get('p_code')
        user = request.user
        try:
            promo_code = PromoCode.objects.get(code=p_code)
        except ObjectDoesNotExist:
            messages.error(request, "INVALID CODE")
            return redirect('store')

        if promo_code.max_use:
            if promo_code.times_used >= promo_code.max_use:
                messages.error(request, "Sorry, this code has been exhausted ")
                return redirect('profile', user.username)
            elif promo_code.has_expired:
                messages.error(request, "Sorry this code has expired")
                return redirect('profile', user.username)
            else:

                try:
                    UserPromoCode.objects.create(user=user, code=promo_code)
                except IntegrityError:
                    messages.error(request, 'Sorry You have already used this code')
                    return redirect('profile', user.username)
                
                if promo_code.purpose == 'Token':
                    user.tokens.amount += promo_code.token_amount
                    user.tokens.save()
                    messages.success(request, f"Code Redeemed, {promo_code.token_amount} tokens added, you now have {user.tokens.amount} tokens!")
                    return redirect('profile', user.username)

                elif promo_code.purpose == 'Subscription':
                    expires = datetime.now() + timedelta(promo_code.subscription_duration)
                    user.subscription.set_paid_until(expires) 
                    user.subscription.save()
                    messages.success(request, f"Code Redeemed, Your subscription has been extended by {promo_code.subscription_duration} days!")
                    return redirect('profile', user.username)


class DeleteCode(DeleteView):
    model = PromoCode

    def get_success_url(self):
        return reverse('code_gen')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    