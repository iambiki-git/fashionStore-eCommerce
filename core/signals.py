from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib import messages
from django.utils.timezone import now

@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    #show a welcome msg to user
    #messages.success(request, f"Welcome back, {user.first_name}!")
    # Check if the user is new (you can modify the condition based on your needs)
    if user.date_joined.date() == now().date():  # User is logging in the same day they signed up
        messages.success(request, f"Welcome to our site, {user.first_name}! Enjoy shopping.")
    else:
        messages.success(request, f"Welcome back, {user.first_name}! Glad to have you again.")
