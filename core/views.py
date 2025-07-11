from django.shortcuts import render
from django.views.generic import View


# Create your views here.
class Home(View):
    def get(self, request):
        context = {
        }
        return render(request, 'home.html', context)
    
class Contact(View):
    def get(self, request):
        context = {
        }
        return render(request, 'contact.html', context)