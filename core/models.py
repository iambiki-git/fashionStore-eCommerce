from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} > {self.name}"
    

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex', blank=True, null=True)
    available_colors = models.JSONField(default=list)  # Stores colors as a list
    available_sizes = models.JSONField(default=list) 
    created_at = models.DateTimeField(auto_now_add=True)


    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductPrice(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.new_price}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"
    
from django.conf import settings
class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='wishlisted_by'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') # prevents duplicate 
        ordering = ['-added_at'] # latest first

    def __str__(self):
        return f"{self.user.username}'s wishlist item:- {self.product.name}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    total_price = models.DecimalField(
            max_digits=10,      # Total number of digits, including decimal part
            decimal_places=2,   # Number of digits after the decimal point
            default=0.00,       # Default value for the field
            null=True,          # Allow null value if no price is set
            blank=True          # Allow blank field in forms
        )
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product', 'size')  # Prevents duplicates

    def __str__(self):
        size_display = f"(Size: {self.size})" if self.size else ""
        return f"{self.quantity}x {self.product.name} {size_display}"
