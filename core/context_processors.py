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


