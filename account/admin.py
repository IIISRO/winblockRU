from django.contrib import admin
from .models import User, Basket, BasketItem

# Register your models here.

admin.site.register(User)

admin.site.register(Basket)

admin.site.register(BasketItem)
