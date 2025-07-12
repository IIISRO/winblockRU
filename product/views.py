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
        sort = request.GET.get('sort')
        products = Product.objects.all()

        if sort == 'latest':
            products = products.order_by('-created_at')  # or '-id' if you don’t have a timestamp
        elif sort == 'price_low':
            products = products.order_by('price')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'title':
            products = products.order_by('title')

        context = {
            'products': products,
            'current_sort': sort
        }
        return render(request, 'shop.html', context)
