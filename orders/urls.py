from django.urls import path
from .views import checkout_view, order_complete_view,track_order_view

app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('thank-you/', order_complete_view, name='order_complete'),
    
    path('track-order/', track_order_view, name='track_order'),
]
