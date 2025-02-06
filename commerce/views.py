from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from commerce.models import *
from typing import Optional
from commerce.forms import *

# //////////////////// P R O D U C T //// C R U D ////////////////////
def product_list(request):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')

    if filter_type == 'date':
        products = Product.objects.all().order_by('-created_at')
    elif filter_type == 'price':
        products = Product.objects.all().order_by('-price')
    elif filter_type == 'rating':
        products = Product.objects.all().order_by('-rating')

    else:
        products = Product.objects.all()

    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    context = {
        'products': products,
    }
    return render(request, 'commerce/Products/product-list.html', context=context)

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product=product, is_negative=False)
    formatted_date = product.created_at.strftime("%B %d, %Y")

    context = {
        'product': product,
        'comments': comments,
        'formatted_date': formatted_date,
    }
    return render(request, 'commerce/Products/product-details.html', context)

def comment_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_details', product_id=pk)

        else:
            print(form.errors)

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'commerce/Products/product-details.html', context=context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been successfully added.')
            return redirect('product_list')
    else:
        form = ProductModelForm()

    categories = Category.objects.all()
    context = {
        'form': form,
        'categories': categories
    }

    return render(request, 'commerce/Products/add_product.html', context=context)

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        form = ProductModelForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('customer_list')
    else:
        form = ProductModelForm(instance=product)

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'form': form
    }

    return render(request, 'commerce/Products/edit_product.html', context=context)

# //////////////////// C U S T O M E R //// C R U D ////////////////////
def customer_list(request):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')

    if filter_type == 'filter':
        customers = Customer.objects.all().order_by('full_name')
    else:
        customers = Customer.objects.all().order_by('-created_at')

    for customer in customers:
        customer.created_date = customer.created_at.strftime("%B %d, %Y")

    if search_query:
        customers = Customer.objects.filter(full_name__icontains=search_query)

    context = {
        'customers': customers,
    }

    return render(request, template_name='commerce/customers/customers.html', context=context)

def customer_details(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    created_date = customer.created_at.strftime("%b %d, %I:%M %p")

    context = {
        'customer': customer,
        'created_date': created_date,
    }

    return render(request, template_name='commerce/customers/customer-details.html', context=context)

@login_required
def add_customer(request):
    if request.method == "POST":
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.invoice_prefix = generate_invoice_prefix()
            customer.invoice_number = 1
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerModelForm()

    return render(request, 'commerce/Customers/add_customer.html', {'form': form})

@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)

    if request.method == "POST":
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerModelForm(instance=customer)

    return render(request, 'commerce/Customers/edit_customer.html', {'form': form})

@login_required
def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return redirect('customer_list')
    except Customer.DoesNotExist as e:
        print(e)

def order_list(request):
    return render(request, template_name='commerce/Orders/order-list.html')

def order_details(request, order_id):
    return render(request, template_name='commerce/Orders/order-details.html')

def your_view(request):
    objects = Product.objects.all()
    paginator = Paginator(objects, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "commerce/Products/product-list.html", {"page_obj": page_obj})


def about(request):
    return render(request, 'commerce/about.html')


@login_required
def add_to_favourites(request, pk):
    product = get_object_or_404(Product, id=pk)
    favourite, created = Favourite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favourite.delete()
        return redirect('product_list')

    return redirect('product_list')