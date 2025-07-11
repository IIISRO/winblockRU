from django.urls import path
from .views import Home
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),


]