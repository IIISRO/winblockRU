# from django.contrib import messages
# from .helpers import send_forget_pwd,send_activate_link
# from django.template.loader import get_template
# from django.utils.translation import gettext_lazy as _
# import uuid
# from social_django.models import UserSocialAuth
# from django.utils.http import urlsafe_base64_decode
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_str    
# from products.models import Product
# from .tokens import account_activation_token
import json
from django.http import JsonResponse, HttpResponse,Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from product.models import Product
from .models import Basket , BasketItem


User = get_user_model()

# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('core:home'))
    else:
        if request.method == "POST":
            data = json.loads(request.body.decode("utf-8"))
            email = data['email']
            password = data['password']
            user = User.objects.filter(email=email)
            if user.exists():
                user = user.first()
                if authenticate(request, username=user.username, password=password) is None:
                    return JsonResponse({"status": "fail", "message": "Geçersiz kullanıcı adı veya şifre"}, status=401)
                login(request, user)
                return JsonResponse({"status": "success", "message": "Giriş başarılı"})
            else:
                return JsonResponse({"status": "fail", "message": "Geçersiz kullanıcı adı veya şifre"}, status=401)
           
          
        return render(request,'login.html',  context={'error':12})

@login_required()
def logout_user(request):
    logout(request)
    return redirect(reverse_lazy('core:home'))

    
def register(request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("core:home"))

        if request.method == 'POST':
            data = json.loads(request.body.decode("utf-8"))

            first_name = data['firstname']
            last_name = data['lastname']
            email = data['email']
            password = data['password']
            number = data['phone']
            postal = data['post']
            city = data['city']
            address = data['address']

            if not User.objects.filter(email = email).exists():
                user = User.objects.create(
                    username = number.replace('+7','').replace(' ', ''),
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    number = number,
                    postal = postal,
                    cities = city,
                    address = address
                    )
                user.set_password(password)
                user.save()
                return JsonResponse({'status': 'success', 'message': 'Registred user!'},status=200)


            else:     
                return JsonResponse({'status': 'error', 'message': 'Exists user!'},status=400)
        
        return render(request,'register.html')


@login_required()
def add_basket(request, prodid, colorid, gridid):
    if request.method  == "POST":
        if Basket.objects.filter(user=request.user).exists():
            basket =  Basket.objects.get(user = request.user)
        else:
            basket = Basket.objects.create(user = request.user)

        prodid = int(prodid)
        gridid = int(gridid)
        colorid = int (colorid)

        if colorid < 0:
            colorid = None
        if gridid < 0:
            gridid = None

        if BasketItem.objects.filter(basket=basket, product_id = prodid, color_id = colorid, grid_id = gridid).exists():
            item = BasketItem.objects.get(basket=basket, product_id = prodid, color_id = colorid, grid_id = gridid)
            item.quantity += 1
            item.save()
        else:
            BasketItem.objects.create(
                basket = basket,
                product_id = prodid,
                color_id = colorid,
                grid_id = gridid
                )
        

        return JsonResponse({'status': 'success', 'message': 'Added'},status=200)

@login_required()
def cart(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    products = []
    if Basket.objects.filter(user=request.user).exists():

        products = Basket.objects.get(user=request.user).basketitem_set.all()
        for product in products:
            print(product.product)
    context = {
        'products' : products
    }
    return render(request, 'cart.html', context)




@login_required
def update_basket(request, id):
    data = json.loads(request.body.decode("utf-8"))
    item = BasketItem.objects.get(id = id)

    if data['action'] == 'delete':
        item.delete()
    elif data['action'] == 'add':
        item.quantity += 1
        item.save()
    else:
        if item.quantity > 0:
            item.quantity -= 1
            item.save()
        if item.quantity == 0:
            item.delete()
            
    return JsonResponse({'status': 'success', 'message': 'Added'},status=200)