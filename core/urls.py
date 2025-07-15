from django.urls import path
from .views import Home,dealer_list,contact_view
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('contact/', contact_view, name='contact'),
    path('dealer_list/', dealer_list, name='dealer_list'),


]