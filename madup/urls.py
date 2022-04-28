from django.urls import path, include
import advertisers.urls, ads.urls

urlpatterns = [
    path('api/v1/ads/', include(ads.urls)),
    path('api/v1/advertisers/', include(advertisers.urls)),
]
