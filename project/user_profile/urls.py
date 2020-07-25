from django.urls import path, include
from user_profile.views import ProfileView

urlpatterns = [
    path("<username>/", ProfileView.as_view(), name='profile')
    ]