from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def home(request):
    """
    Renders the homepage with a list of all products
    """
    products = Product.objects.all()  # all products
    context = {
        'products': products
    }
    return render(request, 'products/home.html', context)

def category(request, foo):
    # Convert '_' to space for URL-friendly category names
    normalized = foo.replace('_', ' ').replace('_', ' ').strip()
    # Grab the category from the url
    try:
        # Match category case-insensitively
        category = Category.objects.get(name__iexact=normalized)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'products': products,
            'category': category
        })

    except Category.DoesNotExist:
        messages.error(request, ("The Category does not exist, try again"))
        return redirect('home')


def product_detail(request, product_id):
    """
    Renders the detail page for a single product
    """
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'products/product.html', context)

def about(request):
    return render(request, 'about.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
          login(request, user)
          messages.success(request, ("You have been Logged in."))
          return redirect('home')
        else:
          messages.error(request, ("There was an error, try again"))
          return redirect('login')
    else:
        return render(request, 'login_user.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login') 

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, ("You are registered."))
            return redirect('login')
        else:
            messages.success(request, ("Sorry! registration not successful."))
            return redirect('register')  
    else:
        return render(request, 'register_user.html', {'form':form})
