from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from bookmarker.views import index, red, get_secret_page, generate_secret_link, admin_page
from django.conf import settings
from django.conf.urls.static import static


# defines the urls (links) 
urlpatterns = [
    path("", red, name="red"),
    path('watch/', index, name='index'),
    path("admin/", admin_page, name="admin_page"),
    path("generate/", generate_secret_link, name="generate" ),
    path("login/", LoginView.as_view(template_name='bookmarker/login.html'), name="login"),
    path("logout/", LogoutView.as_view(template_name='bookmarker/index.html'), name="logout"),
    path("<slug:link>/", get_secret_page, name="secret"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


