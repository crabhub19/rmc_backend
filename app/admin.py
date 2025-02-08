from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *
# Register your models here.
class ProductAdmin(ModelAdmin):
    pass
class CategoryAdmin(ModelAdmin):
    pass
class BrandAdmin(ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)