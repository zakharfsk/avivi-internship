from django.urls import path

from . import views

app_name = 'telegram_bot'

urlpatterns = [
    path('', views.TelegramBotListView.as_view(), name='telegram_bots'),
    path('page/<int:page>/', views.TelegramBotListView.as_view(), name='telegram_bots_paginator'),
    path('create/', views.TelegramBotCreateView.as_view(), name='telegram_bots_create'),
    path('<int:pk>/', views.TelegramBotDetailView.as_view(), name='telegram_bots_detail'),
    path('<int:pk>/update/', views.TelegramBotUpdateView.as_view(), name='telegram_bots_update'),
    path('<int:pk>/delete/', views.TelegramBotDeleteView.as_view(), name='telegram_bots_delete'),
]
