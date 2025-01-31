from django.contrib import admin
from django.urls import path, include
from commerce import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('detail/<int:product_id>/',views.product_details, name='product_details' ),
    path('order_list/', views.order_list, name='order_list'),
    path('order_detail/<int:order_id>/',views.order_details, name='order_details' ),
]