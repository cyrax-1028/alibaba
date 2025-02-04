from django.shortcuts import render, get_object_or_404
from commerce.models import *

def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, template_name='commerce/product-list.html', context=context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'commerce/product-details.html', context)

def order_list(request):
    return render(request, template_name='commerce/order-list.html')

def order_details(request, order_id):
    return render(request, template_name='commerce/order-details.html')