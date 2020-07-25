from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

# Create your views here.

class ProfileView(DetailView):
    model = User
    template_name = 'user_profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))
