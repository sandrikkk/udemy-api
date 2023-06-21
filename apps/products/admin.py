from django.contrib import admin
from apps.products.models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product",)}


admin.site.register(Product, ProductAdmin)
