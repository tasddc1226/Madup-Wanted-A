from django.urls import path, include
import advertisers.urls, ads.urls

urlpatterns = [
    path('', include(ads.urls)),
    path('advertisers', include(advertisers.urls)),
]
