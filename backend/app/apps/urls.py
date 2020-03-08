from django.urls import path, include

urlpatterns = [
    path('authentication/', include('app.apps.authentication.urls', namespace='authentication')),
    path('hotels/', include('app.apps.hotels.urls', namespace='hotels')),
]
