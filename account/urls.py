from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('cart/', cart, name='cart'),

    re_path(r'^addbasket/(?P<prodid>-?\d+)/(?P<colorid>-?\d+)/(?P<gridid>-?\d+)/$', add_basket, name='addbasket'),
    
    path('update_basket/<int:id>/', update_basket, name='update_basket'),
    # path('profile/', Profile.as_view(), name='profile'),
    # path('register/', Signin.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
     path('forget-password/', forget_password, name='forget_password'),
    path('reset/<uidb64>/<token>/', reset_password, name='reset_password'),

    


]