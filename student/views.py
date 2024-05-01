from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from student.forms import LoginForm, StudentForm
from student.models import Student, User
from django.conf import settings
import os
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
EMAIL_HOST_USER = settings.EMAIL_HOST_USER
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login_view')  # Redirect to a URL configured in settings
        else:
            return render(request, 'student/register.html', {'error_message': 'Invalid Data', 'form': form })
    else:
        return render(request, 'student/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        print("login form submitted")
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"{username}   |   {password}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a URL configured in settings
            else:
                return render(request, 'student/login.html', {'error_message': 'Invalid username/password.', 'form': form})
    else:
        form = LoginForm()
        return render(request, 'student/login.html', {'form': form})


def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login_view')  # Redirect them to the login page, or wherever you prefer


def profile(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        student = Student.objects.get(user__id=request.user.id)
        return render(request, 'student/profile.html', {'student': student})
    else:
        return redirect('home')


def edit_profile(request):
    if request.user.is_authenticated and request.user.groups.filter(name='Student').exists():
        if request.method == 'POST':
            photo = request.FILES if request.FILES else None
            request_query_dict_data = request.POST
            data = request_query_dict_data.dict()
            # print(data)
            student = {
                "username": request.user.username,
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email'],
                "date_of_birth": data['date_of_birth'],
                "address": data['address'],
                "city_town": data['city_town'],
                "country": data['country']
            }
            student_ = Student.objects.get(user__username=request.user.username)
            user_obj = User.objects.filter(username=request.user.username).update(
                first_name=student['first_name'],
                last_name=student['last_name'],
                email=student['email'],
            )
            student_obj = Student.objects.filter(user__username=request.user.username).update(
                address=student['address'],
                date_of_birth=student['date_of_birth'],
                city_town=student['city_town'],
                country=student['country']
            )

            if photo:
                photo = photo.dict()
                old_image = student_.photo
                if old_image:
                    old_image_path = os.path.join(settings.MEDIA_ROOT, str(student_.photo))
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                        student_.photo = photo['photo']
                        student_.save()
        student = Student.objects.get(user__id=request.user.id)
        return render(request, 'student/edit_profile.html', {'student': student})
    else:
        return redirect('home')



# password reset
def passwordResetEmail(request):
    if request.method == 'POST':
        current_domain = request.META['HTTP_HOST']
        message = None
        email = request.POST.get('password_reset_email')
        print('email : ', email)
        user = None
        try:
            user = User.objects.get(email=email)
            print(user)
            send_email_flag = passwordResetSendMail(user.id, current_domain)
            if send_email_flag:
                message = 'We have send a password reset email to you.'
            else:
                message = 'Invalid email address'
        except User.DoesNotExist:
            message = 'Invalid email address'
            print(message)
        return render(request, 'student/password_reset.html', {"message": message})
    else:
        return render(request, 'student/password_reset.html')


def passwordResetSendMail(id, current_domain):
    user = User.objects.get(pk=id)
    email_context = {
        'id': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user),
        'domain': current_domain
    }
    subject = 'Password reset request - Logo Animations '
    # html_message = render_to_string('accounts/password_reset_email.html', email_context)
    html_message = render_to_string('student/password_reset_email_template.html', email_context)

    email_from = EMAIL_HOST_USER
    recipient_list = [user.email]
    message = EmailMessage(subject, html_message, email_from, recipient_list)
    message.content_subtype = 'html'
    try:
        message.send()
        return True
    except:
        return False



def passowrdResetForm(request, uidb64, token):
    if request.method == 'POST':
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)

        password_one = request.POST.get('signup_pasword')
        password_two = request.POST.get('signup_confirm')
        
        if user is not None and default_token_generator.check_token(user, token):
            if password_one == password_two:
                user.set_password(password_one)
                user.save()
                message = 'Password changed successfully.'
                print('message: ', message)
            else:
                message = "Password doesn't match."
        else:
            message = 'Invalid link.'
        return render(request, 'student/password_reset_form.html', {'message': message})
    else:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'student/password_reset_form.html')
        message = 'Invalid link.'
        return render(request, 'student/password_reset_form.html', {'message': message})


@login_required(login_url=reverse_lazy('login'))
def change_password(request):
    message = None
    if request.method == 'POST':
        password = request.POST.get('password', None)
        password_one = request.POST.get('confirm_password', None)
        if password_one != None and password_one == password:
            user = User.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()
            message = "Password Changed Successfully!"
        else:
            message = "Password doesn't match."
    return render(request, 'student/change_password.html', {'message': message})