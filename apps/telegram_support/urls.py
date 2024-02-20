from django.urls import path

from . import views

app_name = 'telegram_support'

urlpatterns = [
    path('tickets/', views.SupportTicketsListView.as_view(), name='tickets'),
    path('tickets/page/<int:page>/', views.SupportTicketsListView.as_view(), name='tickets_paginator'),
]
