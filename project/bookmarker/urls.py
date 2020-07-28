from django.urls import path, include
from bookmarker.views import Index, red, generate_secret_link, admin_page, Count, StoreView, BuyToken, Subscribe
from django.conf import settings
from django.conf.urls.static import static


# defines the urls (links) 
urlpatterns = [
    path("", red, name="red"),
    path('watch/', Index.as_view(), name='index'),
    path("site/admin/", admin_page, name="admin_page"),
    path("generate/", generate_secret_link, name="generate" ),
    path('view_counter/', Count.as_view(), name='view_counter' ),
    path('store/', StoreView.as_view(), name='store'),
    path('buy_tokens', BuyToken.as_view(), name='buy_tokens'),
    path('subscribe/', Subscribe.as_view(), name="subscribe")


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


