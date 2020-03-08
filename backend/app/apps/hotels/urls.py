from django.urls import path
from .views import ListHotelsView, SingleHotelsView, RecommendationView, Dashboard, AddHotel
app_name = 'hotels'

urlpatterns = [
path('', ListHotelsView.as_view(), name="list-hotels"),
path('hotel/<str:hotel_id>', SingleHotelsView.as_view(), name="hotel-detail"),
path('recommendation', RecommendationView.as_view(), name="hotel-recommendation"),
path('dashboard', Dashboard.as_view(), name="dashboard"),
path('hotel', AddHotel.as_view(), name="add-hotel"),
]
