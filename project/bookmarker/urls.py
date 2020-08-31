from django.urls import path, include
from bookmarker.views import Index, red, Count, StoreView, BuyToken, Subscribe, IndexBeta, ActivateVoicePause, ActivateVoicePlay, SetAutoPauseView, SetManualPauseView
from django.conf import settings
from django.conf.urls.static import static


# defines the urls (links) 
urlpatterns = [
    path("", red, name="red"),
    path('view_counter/', Count.as_view(), name='view_counter'),
    path('store/', StoreView.as_view(), name='store'),
    path('buy_tokens', BuyToken.as_view(), name='buy_tokens'),
    path('subscribe/', Subscribe.as_view(), name="subscribe"),
    path('activate_voice_pause/', ActivateVoicePause.as_view(), name="activate_voice_pause"),
    path('activate_voice_play/', ActivateVoicePlay.as_view(), name="activate_voice_play"),
    path('auto_pause/', SetAutoPauseView.as_view(), name="auto_pause"),
    path('manual_pause/', SetManualPauseView.as_view(), name="manual_pause"),
    



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.BETA:
    urlpatterns.append(path('watch/', IndexBeta.as_view(), name='index'))
else:
    urlpatterns.append(path('watch/', Index.as_view(), name='index'))
