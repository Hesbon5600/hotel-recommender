from django.urls import path
from .views import UserLoginCreateView, UserRegistrationCreateView,logout_view

app_name = 'authentication'

urlpatterns = [
    path('login', UserLoginCreateView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', UserRegistrationCreateView.as_view(), name='signup'),
]
