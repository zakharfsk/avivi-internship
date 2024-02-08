from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.user import views

app_name = 'user'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationCreateView.as_view(), name='register'),

    path('profile/', login_required(views.UserProfileView.as_view()), name='profile'),

    path('tg_users/', login_required(views.ListTelegramUserListView.as_view()), name='tg_users'),
    path('tg_users/page/<int:page>/', login_required(views.ListTelegramUserListView.as_view()), name='tg_users_paginator'),
    path('tg_users/create/', login_required(views.CreateTelegramUserCreateView.as_view()), name='tg_users_create'),
    path('tg_users/<int:pk>/', login_required(views.DetailTelegramUserDetailView.as_view()), name='tg_users_detail'),
    path('tg_users/<int:pk>/update/', login_required(views.UpdateTelegramUserUpdateView.as_view()), name='tg_users_update'),
    path('tg_users/<int:pk>/delete/', login_required(views.DeleteTelegramUserDeleteView.as_view()), name='tg_users_delete'),
]
