from django.urls import path
from promo_code.views import CodeGen, UseCode

urlpatterns = [
    path('', CodeGen.as_view(), name="code_gen"),
    path('redeem/', UseCode.as_view(), name='redeem'),
]
