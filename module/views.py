from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'module/home.html')


def about_us(request):
    return render(request, 'module/about_us.html')


def contact_us(request):
    return render(request, 'module/contact_us.html')


def list_modules(request):
    return render(request, 'module/list_modules.html')