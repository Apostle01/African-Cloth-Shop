from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, UserInfoForm, UpdatePasswordForm
from django import forms
from .models import Profile
# from django.db.models import Q
from products.models import Product   


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
    
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # log in user
            user = authenticate(username=username, password=password)
            login(request,user)

            messages.success(request, ("Username  created, fill out your info below."))
            return redirect('update_info')
        else:
            messages.error(request, ("Sorry! registration not successful."))
            return render(request, 'register_user.html', {'form':form})  
    else:
        form = SignUpForm()
        return render(request, 'register_user.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User is Upodated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You must login to access page!!")
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user_id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)

        if form.is_valid():
            form.save()

            messages.success(request, "User Info is Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form})
    else:
        messages.success(request, "You must login to access page!!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # ----------------------
        # If form is submitted
        # ----------------------
        if request.method == 'POST':
            form = UpdatePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully!")
                return redirect('home')
            else:
                messages.error(request, "Please correct the errors below.")
                return render(request, "update_password.html", {'form': form})

        # ----------------------
        # If GET request
        # ----------------------
        else:
            form = UpdatePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})

    else:
        messages.error(request, "You must login to access page!!")
        return redirect('login')

def search(request):
    if request.method == "POST":
        query = request.POST.get('searched', '').strip()

        # If user submits an empty search
        if query == "":
            messages.error(request, "Please enter a search term.")
            return render(request, "search.html", {})

        # Search products
        results = Product.objects.filter(category__name__icontains=query)

        # No results found
        if not results.exists():
            messages.error(request, "No products found. Try another search term.")
            return render(request, "search.html", {"query": query})

        # Return page with results
        return render(request, "search.html", {
            "query": query,
            "results": results,
        })

    return render(request, "search.html", {})


# def search(request):
#     # Determine if they filled out the form
#     if request.method =="POST":
#         searched = request.POST.get('searched', '')

#         # Query The Products DB Model
#         searched = Product.objects.filter(name__icontains=searched)
#         # Test for null
#         if not searched:
#             messages.success(request, "The product does not exist. Try another one!")
#             return render(request, 'search.html', {})

#         else:
#             return render(request, "search.html", {'searched':searched })
#     else:
#         return render(request, "search.html", {})
