from django.urls import path
from core import views


urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.registration_view, name='registration'),
    

    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.products, name='products'),
    path('my-account/', views.myAccount, name='myAccount'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
