from django.contrib import admin

from .models import Category, Product, LineItem, Cart

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ["name"]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "date_created", "description", "price", "category"]


admin.site.register(Product, ProductAdmin)


class LineItemAdmin(admin.ModelAdmin):
    fields = ["product", "quantity", "price", "cart"]


admin.site.register(LineItem, LineItemAdmin)


class CartAdmin(admin.ModelAdmin):
    fields = ["total_price"]


admin.site.register(Cart, CartAdmin)