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
from product.models import Product, Color, Grid

User = get_user_model()

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
            return JsonResponse({"status": "fail", "message": "Пользователь не найден"}, status=401)

        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)
            return JsonResponse({"status": "success", "message": "Вход выполнен успешно"})
        else:
            return JsonResponse({"status": "fail", "message": "Неверный пароль"}, status=401)

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

        if not User.objects.filter(email=email).exists():
            user = User.objects.create(
                username=number.replace('+7', '').replace(' ', ''),
                first_name=first_name,
                last_name=last_name,
                email=email,
                number=number,
                postal=postal,
                cities=city,
                address=address
            )
            user.set_password(password)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'Пользователь зарегистрирован!'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Пользователь уже существует!'}, status=400)

    return render(request, 'register.html')


@login_required()
def add_basket(request, prodid, colorid, gridid):
    if request.method == "POST":
        try:
            quantity = 1
            basket, _ = Basket.objects.get_or_create(user=request.user)

            product = get_object_or_404(Product, id=prodid)

            color = None
            if str(colorid).isdigit() and int(colorid) >= 0:
                color = Color.objects.filter(id=colorid).first()

            grid = None
            if str(gridid).isdigit() and int(gridid) >= 0:
                grid = Grid.objects.filter(id=gridid).first()

            item, created = BasketItem.objects.get_or_create(
                basket=basket,
                product=product,
                color=color,
                grid=grid,
                defaults={"quantity": quantity}
            )

            if not created:
                item.quantity += quantity
                item.save()

            return JsonResponse({'status': 'success', 'message': 'Добавлено'}, status=200)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=405)


@login_required()
def cart(request):
    basket_items = BasketItem.objects.filter(basket__user=request.user)

    subtotal = sum(item.total_price for item in basket_items)
    shipping = 10 
    total = subtotal + shipping

    context = {
        'products': basket_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    }
    return render(request, 'cart.html', context)


@login_required
def update_basket(request, id):
    data = json.loads(request.body.decode("utf-8"))
    item = BasketItem.objects.get(id=id)

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

    return JsonResponse({
        'status': 'success',
        'message': 'Обновлено',
        'cart_count': BasketItem.objects.filter(basket__user=request.user).count()
    }, status=200)


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
                subject="Сброс пароля",
                message="",
                from_email=None,
                recipient_list=[user.email],
                html_message=html
            )
            return JsonResponse({'status': 'ok', 'message': 'Ссылка для сброса отправлена'})
        return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'}, status=404)

    return render(request, 'forget_password.html')


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
            return JsonResponse({'status': 'ok', 'message': 'Пароль успешно сброшен'})
        return JsonResponse({'status': 'fail', 'message': 'Неверная или устаревшая ссылка'}, status=400)

    return render(request, 'reset_password.html', {
        'validlink': user and account_activation_token.check_token(user, token)
    })
