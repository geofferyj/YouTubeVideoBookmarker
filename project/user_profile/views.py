from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.utils import timezone as tz

# Create your views here.

class ProfileView(DetailView):
    model = User
    template_name = 'user_profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    # def get_context_data(self, **kwargs):
    #     user = self.get_object()
    #     context = super().get_context_data(**kwargs)
    #     end_date = user.subscription.date_created + tz.timedelta(days=user.subscription.duration)
    #     context["end_date"] = end_date
    #     return context
    
    
    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return user
 