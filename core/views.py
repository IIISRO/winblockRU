from django.shortcuts import render, redirect
from django.views.generic import View
from product.models import Product
from django.conf import settings
import json
import os
from .models import Contact
from django.contrib import messages


class Home(View):
    def get(self, request):
        latest_products = Product.objects.all().order_by('-created_at')[:8]  
        context = {
            'latest_products': latest_products
        }
        return render(request, 'home.html', context)


def dealer_list(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'core', 'data', 'data.json')

    dealers = []
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            dealers = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: dealers.json не найден по пути {json_file_path}")
    except json.JSONDecodeError:
        print(f"Ошибка: не удалось декодировать JSON из {json_file_path}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

    context = {
        'dealers': dealers,
        'page_title': 'Список дилеров (за рубежом)'
    }
    return render(request, 'dealer_list.html', context) 


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
            messages.success(request, "Ваше сообщение было успешно отправлено!")
            return redirect('core:contact')
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")

    return render(request, 'contact.html')
