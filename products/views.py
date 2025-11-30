from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



def home(request):
    """
    Renders the homepage with a list of all products
    """
    products = Product.objects.all()  # all products
    context = {
        'products': products
    }
    return render(request, 'products/home.html', context)

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
            
# def login_user(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login Successful!")
#             return redirect("/")  # Redirect to homepage
#         else:
#             messages.error(request, "Invalid username or password")
#             return redirect("/login/")

#     return render(request, "login_user.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
