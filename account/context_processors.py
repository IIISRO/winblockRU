from .models import BasketItem

def cart_count(request):
    if request.user.is_authenticated:
        return {
            'cart_count': sum(item.quantity for item in BasketItem.objects.filter(basket__user=request.user))
        }
    
    return {'cart_count': 0}
