from .models import Wishlist, Cart

def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}


def cart_item_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}


from decimal import Decimal, ROUND_HALF_UP  
def cart_totals(request):
    subtotal = Decimal('0.00')
    shipping = Decimal('0.00')
    total = Decimal('0.00')
    discount = Decimal('0.00')

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        # Calculate subtotal
        for item in cart_items:
            subtotal += item.total_price  # Assumes total_price is Decimal

        # Shipping
        shipping = Decimal('100.00') if subtotal < Decimal('1000.00') else Decimal('0.00')

        # Total before discount
        total = subtotal + shipping

        # Discount based on total
        if total > Decimal('10000.00'):
            discount = total * Decimal('0.50')
        elif total > Decimal('5000.00'):
            discount = total * Decimal('0.20')
        elif total > Decimal('3000.00'):
            discount = total * Decimal('0.10')  

        discount = discount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total = (total - discount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        shipping = shipping.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    return {
        'cart_subtotal': subtotal,
        'cart_shipping': shipping,
        'cart_discount': discount,
        'cart_total': total,
    }
