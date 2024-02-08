from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.user import views

app_name = 'user'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationCreateView.as_view(), name='register'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),

    path('tg_users/', views.TelegramUserListView.as_view(), name='tg_users'),
    path('tg_users/page/<int:page>/', views.TelegramUserListView.as_view(), name='tg_users_paginator'),
    path('tg_users/create/', views.TelegramUserCreateView.as_view(), name='tg_users_create'),
    path('tg_users/<int:pk>/', views.TelegramUserDetailView.as_view(), name='tg_users_detail'),
    path('tg_users/<int:pk>/update/', views.TelegramUserUpdateView.as_view(), name='tg_users_update'),
    path('tg_users/<int:pk>/delete/', views.TelegramUserDeleteView.as_view(), name='tg_users_delete'),
]
