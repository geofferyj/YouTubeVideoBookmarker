from django.urls import path, include
from bookmarker.views import Index, red, get_secret_page, generate_secret_link, admin_page,recog
from django.conf import settings
from django.conf.urls.static import static


# defines the urls (links) 
urlpatterns = [
    path("", red, name="red"),
    path("recog/", recog),
    path('watch/', Index.as_view(), name='index'),
    path("site/admin/", admin_page, name="admin_page"),
    path("generate/", generate_secret_link, name="generate" ),
    path("<slug:link>/", get_secret_page, name="secret"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


