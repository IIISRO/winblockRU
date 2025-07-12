from .models import Product

def product_categories(request):
    kids_products = Product.objects.filter(category='FOR KIDS').distinct()
    animal_products = Product.objects.filter(category='FOR ANIMAL').distinct()
    
    return {
        'kids_products': kids_products,
        'animal_products': animal_products
    }
