from django.urls import path

from apps.user.views import UserLoginView, UserRegistrationCreateView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationCreateView.as_view(), name='register'),
]
