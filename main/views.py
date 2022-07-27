from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from product.models import Product,Category

#  Import Form
from .forms import SignUpForm


#  FBV

# Index view 
def index(request):
    products = Product.objects.all()[0:8] # Slice by 8

    return render(request, 'main/index.html', {'products': products})


# Signup View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # Pass Post details to Form

        if form.is_valid(): # If form is valid, Default django from validation.
            user = form.save() # Save new user

            login(request, user) # Login new user

            return redirect('/') # Redirect to home

    else:
        form = SignUpForm()

    return render(request, 'main/signup.html', {'form': form})


#  My account View
@login_required
def myaccount(request):
    return render(request, 'main/myaccount.html')

# Edit Account View
@login_required
def edit_myaccount(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.save()

        return redirect('myaccount')

    return render(request, 'main/edit_myaccount.html')




# Shop View
def shop(request):
    categories = Category.objects.all() # get all categgories
    products = Product.objects.all() # get all products

    active_category = request.GET.get('category', '') #Get categoriy query

    if active_category: # if Category Query
        products = products.filter(category__slug=active_category) # Filter products by category

    query = request.GET.get('query', '') # Get search query

    if query: # If Search query
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query)) # Filter by Search query

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    } # Context

    return render(request, 'main/shop.html', context)