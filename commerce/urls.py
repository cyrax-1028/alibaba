from django.contrib import admin
from django.urls import path, include
from commerce import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('detail/<int:product_id>/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('product-comments/<int:pk>/', views.comment_view, name='comment_view'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer_detail/<int:pk>/', views.customer_details, name='customer_details'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('edit_customer/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('about/', views.about, name='about'),
    path('add_to_favourites/<int:pk>/', views.add_to_favourites, name='add_to_favourites'),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:order_id>/', views.order_details, name='order_details'),
]