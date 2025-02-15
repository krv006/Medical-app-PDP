from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('medical/', include('medical.urls')),
    path('shops/', include('shops.urls')),
]


