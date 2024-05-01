from django.urls import path
from student.views import *

urlpatterns = [
    path('register', register, name='register'),
    path('login', login_view, name='login_view'),
    path('profile', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('logout', logout_view, name='logout_view'),

        # password reset 
    path('password-reset', passwordResetEmail, name="passwordResetEmail"),
    # password reset link
    path('reset-password/<uidb64>/<token>', passowrdResetForm, name="passowrdResetForm"),
    path('change_password', change_password, name='change_password'),
]