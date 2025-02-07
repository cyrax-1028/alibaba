from django.contrib import admin
from django.urls import path, include
from commerce import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('detail/<int:product_id>/', views.product_details, name='product_details'),
    path('product_grid/', views.product_grid, name='product_grid'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('product-comments/<int:pk>/', views.comment_view, name='comment_view'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer_detail/<int:pk>/', views.customer_details, name='customer_details'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('about/', views.about, name='about'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:order_id>/', views.order_details, name='order_details'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]