from django.shortcuts import render,redirect
from django.views.generic import View
from product.models import Product
from django.conf import settings
import json
import os
from .models import Contact
from django.contrib import messages

# Create your views here.
class Home(View):
    def get(self, request):
        latest_products = Product.objects.all().order_by('-created_at')[:8]  # Show latest 8
        context = {
            'latest_products': latest_products
        }
        return render(request, 'home.html', context)
    
def dealer_list(request):
    """
    Loads dealer data from a JSON file and renders it in a template.
    """
    # Construct the full path to your JSON file
    # Adjust 'data/dealers.json' if your file is located elsewhere
    json_file_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'data.json')

    dealers = []
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            dealers = json.load(f)
    except FileNotFoundError:
        print(f"Error: dealers.json not found at {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    context = {
        'dealers': dealers,
        'page_title': 'Dealer List (Abroad) / Bayi Listesi (Yurt Dışı)'
    }
    return render(request, 'dealer_list.html', context) # Render to a new template name
    



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('core:contact')
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'contact.html')
