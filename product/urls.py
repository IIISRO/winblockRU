from django.urls import path
from .views import ProductDetail, ShopPage
from django.views.generic import TemplateView

app_name = 'product'

urlpatterns = [
    path('shop/', ShopPage.as_view(), name='shop'),
    path('shop/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),



]