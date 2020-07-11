from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from bookmarker.views import index, red, signup
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('watch/', index, name='index'),
    path("", red, name="red"),
    path("register/", signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="bookmarker/register.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
