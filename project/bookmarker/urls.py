from django.contrib import admin
from django.urls import path, include
from bookmarker.views import index, red
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('watch/', index, name='index'),
    path("", red, name="red"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
