from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from account.models import BasketItem  
from datetime import datetime, timedelta
import random

@login_required
def checkout_view(request):
    user = request.user
    products = BasketItem.objects.filter(basket__user=user)
    
    subtotal = sum(item.total_price for item in products)
    shipping = 10  # you can make this dynamic if you want
    total = subtotal + shipping

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')

        order_number = get_random_string(10).upper()

        context = {
            'order_number': order_number,
            'full_name': full_name,
            'address': address,
            'city': city,
            'phone': phone,
            'products': products,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'current_year': datetime.now().year,
        }

        # Render email content
        html_content = render_to_string('checkout_email.html', context)
        text_content = f"""
Thank you for your order!

Order Number: {order_number}
Name: {full_name}
Address: {address}, {city}
Phone: {phone}

Order Details:
"""
        for item in products:
            text_content += f"- {item.product.title} x{item.quantity} = {item.total_price} ₼\n"
        text_content += f"\nSubtotal: {subtotal} ₼\nShipping: {shipping} ₼\nTotal: {total} ₼"

        # Send email
        email = EmailMultiAlternatives(
            subject='Order Confirmation',
            body=text_content,
            from_email='noreply@yourshop.com',
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()


        # Save order summary in session for thank you page
        # Serialize products for session (list of dicts)
        # Serialize products for session (list of dicts)
        products_serialized = []
        for item in products:
            products_serialized.append({
                'product_title': item.product.title,
                'quantity': item.quantity,
                'price': item.product.price,
                'total_price': item.total_price,
            })

    # Clear basket items
        products.delete()

        # Save only serializable data to session
        request.session['order_summary'] = {
            'order_number': order_number,
            'full_name': full_name,
            'address': address,
            'city': city,
            'phone': phone,
            'products': products_serialized,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'current_year': datetime.now().year,
        }

        return redirect('orders:order_complete')

    return render(request, 'checkout.html', {
        'products': products,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })



def order_complete_view(request):
    summary = request.session.pop('order_summary', {})
    print(summary)
    return render(request, 'order_complete.html', {'summary': summary})


FAKE_STATUSES = [
    "Order received",
    "Preparing for shipment",
    "Shipped from warehouse",
    "In transit",
    "Out for delivery",
    "Delivered",
    "Returned",
]



def track_order_view(request):
    order_number = None
    stage = 0
    expected = None

    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        if order_number:
            # Fake simulation; replace with DB logic if needed
            stage = random.randint(1, 3)
            expected = (datetime.now() + timedelta(days=3)).strftime('%A, %B %d')

    return render(request, 'track_order.html', {
        'order_number': order_number,
        'stage': stage,
        'expected': expected
    })