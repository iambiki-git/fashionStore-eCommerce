from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse


# Create your views here.


def index(request):
    return render(request, 'core/index.html')

def registration_view(request):
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

def products(request):
    return render(request, 'core/products.html')


def myAccount(request):
    return render(request, 'core/myAccount.html')


def wishlist(request):
    return render(request, 'core/wishlist.html')

