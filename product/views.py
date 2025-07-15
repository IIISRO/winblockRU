from django.shortcuts import render, get_object_or_404

from django.views.generic import View
from .models import *

class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        colors = product.color.all()
        grids = product.grid.all()
        latest_products = Product.objects.all().order_by('-created_at')[:8]  
        context = {
            
        }
        context = {
            'product': product,
            'colors': colors,
            'grids': grids,
            'default_color': colors[0] if colors else None,
            'default_grid': grids[0] if grids else None,
            'latest_products': latest_products
        }
        return render(request, 'detail.html', context)

    
class ShopPage(View):
    def get(self, request):
        sort = request.GET.get('sort')
        products = Product.objects.all()

        if sort == 'latest':
            products = products.order_by('-created_at') 
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
