from django.contrib import admin
from .models import Product, Variation, Price

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'modified_date', 'is_available', )

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date', )
    list_editable = ('is_active', )

class PricetAdmin(admin.ModelAdmin):
    ordering = ('price',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Price, PricetAdmin)