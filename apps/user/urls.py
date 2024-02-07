from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.user import views

app_name = 'user'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationCreateView.as_view(), name='register'),

    path('profile/', login_required(views.UserProfileView.as_view()), name='profile'),

    path('tg_users/', login_required(views.ListTelegramUser.as_view()), name='tg_users'),
    path('tg_users/page/<int:page>/', login_required(views.ListTelegramUser.as_view()), name='tg_users_paginator'),
    path('tg_users/create/', login_required(views.CreateTelegramUser.as_view()), name='tg_users_create'),
    path('tg_users/<int:pk>/', login_required(views.DetailTelegramUser.as_view()), name='tg_users_detail'),
    path('tg_users/<int:pk>/update/', login_required(views.UpdateTelegramUser.as_view()), name='tg_users_update'),
    path('tg_users/<int:pk>/delete/', login_required(views.DeleteTelegramUser.as_view()), name='tg_users_delete'),
]
