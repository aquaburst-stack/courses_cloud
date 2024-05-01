from django.urls import path
from module.views import *

urlpatterns = [
    path('', home, name='home'),
    path('about_us', about_us, name='about_us'),
    path('contact_us', contact_us, name='contact_us'),
    path('modules', list_modules, name='list_modules'),

    path('courses', courses, name='courses'),
    path('module', module, name='module'),
    path('my_registration', my_registration, name='my_registration'),
]