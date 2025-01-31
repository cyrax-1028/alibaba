from django.shortcuts import render

# Create your views here.

def product_list(request):
    return render(request, template_name='commerce/product-list.html')

def product_details(request, product_id):
    return render(request, 'commerce/product-details.html')

def order_list(request):
    return render(request, template_name='commerce/order-list.html')

def order_details(request, order_id):
    return render(request, template_name='commerce/order-details.html')