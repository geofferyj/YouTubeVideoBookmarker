from django.contrib import admin
from django.urls import path, include
from bookmarker.views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
