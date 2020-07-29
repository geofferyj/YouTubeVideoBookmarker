from django.urls import path
from promo_code.views import CodeGen

urlpatterns = [
    path('', CodeGen.as_view(), name="code_gen")
]
