from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from module.models import Course, Module, Registration, ContactUs
from student.models import Student
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
    code = request.GET.get('code', None)
    register = request.GET.get('register', None)
    is_registered, student = False, None
    if code:
        module = Module.objects.get(code=code)

    if request.user.is_authenticated:
        student = Student.objects.get(user__id=request.user.id)
        if register:
            register = int(register)
            if register == 0:
                Registration.objects.filter(student=student, module=module).delete()
            elif register == 1:
                Registration.objects.create(student=student, module=module)
            return redirect('list_modules')
    modules = Module.objects.all().order_by('-id')
    group, student = False, None
    if request.user.is_authenticated:
        student = Student.objects.get(user_id=request.user.id)
    data = []
    for obj in modules:
        status = False
        if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
            register = Registration.objects.filter(student=student, module=obj).first()
            if register:
                status = True
        data.append({'module': obj, 'status': status})

    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        group = True
    return render(request, 'module/list_modules.html', {'data_obj': data, 'group': group, 'student': student})


# @login_required(login_url=reverse_lazy('login'))
def courses(request):
    id = request.GET.get('id', None)
    is_all, modules = True, None
    courses = Course.objects.all()
    if id:
        courses = courses.filter(id=int(id)).first()
        is_all = False
        modules = courses.modules.all()
    return render(request, 'module/courses.html', {"courses": courses, 'is_all': is_all, 'modules': modules})


def module(request):
    code = request.GET.get('code', None)
    register = request.GET.get('register', None)
    is_registered, student = False, None
    if code:
        module = Module.objects.get(code=code)

    if request.user.is_authenticated:
        student = Student.objects.get(user__id=request.user.id)
        if register:
            register = int(register)
            if register == 0:
                Registration.objects.filter(student=student, module=module).delete()
            elif register == 1:
                Registration.objects.create(student=student, module=module)

        register = Registration.objects.filter(student=student, module=module)
        if register:
            register = register.first()
            if register:
                is_registered = True
    module = Module.objects.filter(code=code).first()
    return render(request, 'module/module.html', {"module": module, "is_registered": is_registered, 'student': student})


@login_required(login_url=reverse_lazy('login'))
def my_registration(request):
    code = request.GET.get('code', None)
    print('code :', code)
    register = request.GET.get('register', None)
    if code:
        module = Module.objects.get(code=code)
        student = Student.objects.get(user__id=request.user.id)
        if int(register) == 1:
            Registration.objects.filter(student=student, module=module).delete()
            return redirect('my_registration')
    registered = Registration.objects.filter(student__user__id=request.user.id)
    return render(request, 'module/my_registration.html', {'registered': registered})