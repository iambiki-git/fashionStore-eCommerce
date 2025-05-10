from django.contrib import admin
from .models import Category, SubCategory, Product, ProductPrice, ProductImage, Wishlist, Cart, ShippingAddress


# Inline for product price
class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    extra = 0

# Inline for product images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'category', 'subcategory', 'is_available', 'stock')
    list_filter = ('gender', 'category', 'subcategory', 'is_available')
    search_fields = ('name', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductPriceInline, ProductImageInline]

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# SubCategory Admin
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_at',)



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'size', 'brand', 'total_price', 'added_on')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_on', 'user')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'contact_number', 'email', 'payment_method', 'created_at')
    search_fields = ('first_name', 'last_name', 'city', 'contact_number')
    list_filter = ('city', 'province')


# Optional: register ProductPrice and ProductImage separately if needed
# admin.site.register(ProductPrice)
# admin.site.register(ProductImage)
