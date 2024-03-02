from django.contrib import admin
from .models import Category, GiftCategory

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug', )
    list_display_links = ('category_name', 'slug', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(GiftCategory)