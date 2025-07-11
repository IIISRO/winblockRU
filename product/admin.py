from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Grid)
admin.site.register(Color)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product, ProductAdmin)