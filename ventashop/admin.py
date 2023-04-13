from django.contrib import admin

from .models import Category, Product

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fields = ["name"]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    fields = ["name", "date_created", "description", "price", "category"]


admin.site.register(Product, ProductAdmin)
