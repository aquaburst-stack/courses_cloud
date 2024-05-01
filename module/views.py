from django.shortcuts import render
from module.models import ContactUs
# Create your views here.


def home(request):
    return render(request, 'module/home.html')


def about_us(request):
    return render(request, 'module/about_us.html')


def contact_us(request):
    message = None
    if request.method == 'POST':
        subject = request.POST.get('subject', None)
        email = request.POST.get('email', None)
        message = request.POST.get('message', None)
        ContactUs.objects.create(subject=subject, email=email, message=message)
        message = 'We have received your message. We will contact you soon.'
    return render(request, 'module/contact_us.html', {'message': message})


def list_modules(request):
    return render(request, 'module/list_modules.html')