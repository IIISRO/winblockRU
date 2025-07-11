from django.shortcuts import render, get_object_or_404

from django.views.generic import View
from .models import *

# Create your views here.
class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug = slug)
        context = {
            'product' : product
        }
        return render(request, 'detail.html', context)
    
class ShopPage(View):
    def get(self, request):
        products = Product.objects.all()
        context = {
            'products' : products
        }
        return render(request, 'shop.html', context)
    
