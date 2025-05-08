from django.urls import path
from core import views


urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration_view, name='registration'),
    

    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/<str:category>/', views.products, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_wishlist_item, name='remove_from_wishlist'),





    path('my-account/', views.myAccount, name='myAccount'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/ajax/', views.add_to_cart, name='add_to_cart_ajax'),


    path('checkout/', views.checkout, name='checkout'),
    path('confirmation/', views.confirmation, name='confirmation'),
]
