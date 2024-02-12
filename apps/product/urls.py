from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('page/<int:page>', views.ProductListView.as_view(), name='products_paginator'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
]
