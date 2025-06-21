from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
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

                #messages.success(request, "Welcome back! You are now logged in.")    
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

    
    # Get IDs of products in user's favorites
    favorite_products = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)


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
        'subcategories': subcategories,
        'favorite_ids': list(favorite_products)

    }

    return render(request, 'core/products.html', context)




from datetime import date, timedelta
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Get product by slug
    product_price = product.price  # Assuming you have a related name 'price' in ProductPrice model
    product_images = product.images.all()  # Assuming you have a related name 'images' in ProductImage model
    preselected_size = request.GET.get('size', '')  # Default to empty string if not provided

    today = date.today()
    estimated_delivery = today + timedelta(days=3)  # You can change 3 to any number of days

    context = {
        'product': product,
        'product_price': product_price,
        'product_images': product_images,
        'estimated_delivery': estimated_delivery.strftime('%a, %b %d'),
        'preselected_size': preselected_size,


    }
    return render(request, 'core/product_detail.html', context)


from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def add_to_wishlist(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'message': 'Added to favorites!'})
        else:
            return JsonResponse({'message': 'Already in favorites.'})
    return JsonResponse({'message': 'Unauthorized or bad request.'}, status=400)



def myAccount(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'core/myAccount.html')


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get the user's wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'core/wishlist.html', context)


# In your Django view:
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@require_POST
@csrf_exempt  # Temporarily for testing, remove in production
def remove_wishlist_item(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    try:
        item = Wishlist.objects.get(id=item_id, user=request.user)
        item.delete()
        return JsonResponse({'status': 'success'}, status=200)
    except Wishlist.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)



def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    cart_items = Cart.objects.filter(user=request.user)

    context = {
        'cart_items':cart_items,

    }
    return render(request, 'core/cart.html', context)



def delete_cart_item(request, item_id):
    # Ensure that the user is logged in (optional check)
    if request.user.is_authenticated:
        user = request.user  # Get the logged-in user

        try:
            # Fetch the cart item to be deleted for the logged-in user
            cart_item = Cart.objects.get(user=user, id=item_id)
            
            # Delete the cart item
            cart_item.delete()

            # Show a success message
            messages.success(request, 'Item deleted successfully!')
        except Cart.DoesNotExist:
            # Show an error message if the item doesn't exist
            messages.error(request, 'Item not found in your cart.')

    else:
        # Redirect to login page if the user is not authenticated
        messages.error(request, 'You need to be logged in to delete items from your cart.')
        return redirect('login')  # Replace with your login page view

    # After deleting, redirect the user back to the cart page
    return redirect('cart')  # Replace with your cart page URL name



from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import F
import json
from .models import Cart, Product

@require_POST
@login_required
def add_to_cart(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_id = data.get('product_id')
        size = data.get('size', 'M')  # Default empty string
        quantity = int(data.get('quantity', 1))  # Default 1

        if not product_id:
            return JsonResponse(
                {'success': False, 'message': 'Product ID is required'},
                status=400
            )

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse(
                {'success': False, 'message': 'Product not found'},
                status=404
            )

        # Check for existing cart items with same product and size
        existing_item = Cart.objects.filter(
            user=request.user,
            product=product,
            size=size
        ).first()

        if existing_item:
            # Update quantity if item exists
            existing_item.quantity = quantity
            existing_item.size = size
            existing_item.total_price=quantity*product.price.new_price
            existing_item.save()
            existing_item.refresh_from_db()
            cart_item = existing_item

            action = 'updated'
        else:
            # Create new item if doesn't exist
            cart_item = Cart.objects.create(
                user=request.user,
                product=product,
                size=size,
                quantity=quantity,
                total_price=quantity*product.price.new_price
            )
            action = 'added'

        cart_count = Cart.objects.filter(user=request.user).count()

        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'message': f'{action.capitalize()} {quantity} x {product.name} to cart (Size: {size if size else "N/A"})',
            'new_quantity': cart_item.quantity,
            'action': action
        })

    except ValueError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid quantity'},
            status=400
        )
    except json.JSONDecodeError:
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON data'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'message': str(e)},
            status=500
        )
    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ajax_update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart_id = data.get("cart_id")
        new_size = data.get("size")
        new_color = data.get("color")

        try:
            cart_item = Cart.objects.get(id=cart_id, user=request.user)

            # Prevent duplicates of same product + size + color
            exists = Cart.objects.filter(
                user=request.user,
                product=cart_item.product,
                size=new_size,
                color=new_color
            ).exclude(id=cart_id).exists()

            if exists:
                return JsonResponse({"success": False, "message": "Same variation already exists in your cart."})

            cart_item.size = new_size
            cart_item.color = new_color
            cart_item.save()
            return JsonResponse({"success": True})
        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "message": "Cart item not found."})
    return JsonResponse({"success": False, "message": "Invalid request."})


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)

    context = {
        'cart_items':cart_items,
    } 
    
    return render(request, 'core/checkout.html', context)



@csrf_exempt
def store_shipping_info(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            
            
            # Create a new ShippingInfo entry (adjust fields as necessary)
            shipping_info = ShippingAddress.objects.create(
                user=request.user,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                address_line1=data['address_line1'],
                address_line2=data['address_line2'],
                city=data['city'],
                province=data['province'],
                contact_number=data['contact_number'],
                payment_method=data['payment_method'],
                delivery_instructions="test",
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


from django.utils import timezone
def confirm_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    shipping_address = ShippingAddress.objects.filter(user=request.user).last()
    

    if request.method == "POST":
        if not shipping_address:
            return redirect('shipping_address_form')  # handle missing address
    
        if not cart_items.exists():
            return redirect('cart')  # or handle empty cart gracefully
        
        # Step 1: Create an Order
        order = Order.objects.create(
            user=request.user,
            order_date=timezone.now(),
            status='PENDING',
            shipping_address=shipping_address
        )

         # Step 2: Create OrderedItems
        for cart_item in cart_items:
            OrderedItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                size=cart_item.size,
                brand=cart_item.brand,
                color="white",
                price_at_purchase=cart_item.product.price.new_price  # or cart_item.product.get_price()
            )

        # Step 3: Clear the cart
        cart_items.delete()

        # Step 4: Redirect to order confirmation page
        return redirect('confirmation')


    context = {
        'cart_items':cart_items,
        'shipping_address':shipping_address,
    }

    return render(request, 'core/confirm_order.html', context)

def confirmation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    order = Order.objects.filter(user=request.user).last()
    shippingAddress = ShippingAddress.objects.filter(user=request.user).last()
    
    
   
    

    context = {
        'order':order,
        'shippingAddress':shippingAddress,
    }

    
    return render(request, 'core/confirmation.html', context)    