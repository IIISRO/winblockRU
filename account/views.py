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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from .models import Basket, BasketItem
from .tokens import account_activation_token
from product.models import Product

User = get_user_model()

# Create your views here.


def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('core:home'))

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data['email']
        password = data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "İstifadəçi tapılmadı"}, status=401)

        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)
            return JsonResponse({"status": "success", "message": "Giriş uğurludur"})
        else:
            return JsonResponse({"status": "fail", "message": "Şifrə yanlışdır"}, status=401)

    return render(request, 'login.html')



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


def forget_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('account:reset_password', kwargs={'uidb64': uid, 'token': token})
            )
            html = render_to_string('email/reset_password_email.html', {
                'user': user,
                'reset_link': reset_link
            })
            send_mail(
                subject="Password Reset",
                message="",
                from_email=None,
                recipient_list=[user.email],
                html_message=html
            )
            return JsonResponse({'status': 'ok', 'message': 'Reset link sent'})
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    return render(request, 'forget_password.html')


# ------------------- RESET PASSWORD -------------------

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        user = None

    if request.method == 'POST':
        data = json.loads(request.body)
        password = data.get('password')

        if user and account_activation_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return JsonResponse({'status': 'ok', 'message': 'Password reset successful'})
        return JsonResponse({'status': 'fail', 'message': 'Invalid or expired link'}, status=400)

    return render(request, 'reset_password.html', {
        'validlink': user and account_activation_token.check_token(user, token)
    })