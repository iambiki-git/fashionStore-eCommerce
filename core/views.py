from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator


# Create your views here.


def index(request):
    return render(request, 'core/index.html')

def registration_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        #GETTING FORM DATA MANUALLY
        full_name = request.POST.get('fullname')
        name_parts = full_name.strip().split(" ", 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        #Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('registration')
        
        #Create new user
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=email,
                email=email,
                password=password
            )
            
            #Automatically log in the user after registration
            login(request, user)
            #messages.success(request, "Registration successful. Please log in.")
            return redirect('index')
        except Exception as e:
            messages.error(request, 'Error creating account : {e}')
            return redirect('registration')
        
    return render(request, 'core/registration.html')


from django.contrib.auth.hashers import check_password
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                login(request, user)

                # Handle "remember me"
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser close

                messages.success(request, "Welcome back! You are now logged in.")    
                return redirect('index')
            else:
                messages.error(request, "Incorrect password")
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No account found with this email")
            return redirect('login')
    
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Come back soon for more amazing deals and updates!")
    return redirect('login')



def products(request, category):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # category_slug = request.GET.get('category') # Get category from URL params
    # subcategory_slug = request.GET.get('subcategory') # Get subcategory from URL params

    # Fetch products based on category and subcategory
    products = Product.objects.all() # Default, show all products

    if category:
        try:
            category = Category.objects.get(slug=category)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            messages.error(request, "Category not found")
            return redirect('products')

    # if category_slug:
    #     category = Category.objects.get(slug=category_slug)
    #     products = products.filter(category=category)

    # if subcategory_slug:
    #     subcategory = SubCategory.objects.get(slug=subcategory_slug)
    #     products = products.filter(subcategory=subcategory)
    
    # Fetch all categories and subcategories for the sidebar or dropdown
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    context = {
        # 'products': products,
        'page_obj': page_obj,
        'categories': categories,
        'subcategories': subcategories
    }

    return render(request, 'core/products.html', context)




from datetime import date, timedelta
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Get product by slug
    product_price = product.price  # Assuming you have a related name 'price' in ProductPrice model
    product_images = product.images.all()  # Assuming you have a related name 'images' in ProductImage model

    today = date.today()
    estimated_delivery = today + timedelta(days=3)  # You can change 3 to any number of days

    context = {
        'product': product,
        'product_price': product_price,
        'product_images': product_images,
        'estimated_delivery': estimated_delivery.strftime('%a, %b %d'),

    }
    return render(request, 'core/product_detail.html', context)




def myAccount(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'core/myAccount.html')


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'core/wishlist.html')


def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'core/cart.html')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    return render(request, 'core/checkout.html')

def confirmation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'core/confirmation.html')    