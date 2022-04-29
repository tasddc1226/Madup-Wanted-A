from django.urls import path
from advertisers.views import AdvertiserSignIn, AdvertiserView

urlpatterns = [
    path('signin', AdvertiserSignIn.as_view()),
    path('<int:advertiser_id>', AdvertiserView.as_view())
]
